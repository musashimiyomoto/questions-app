import secrets
from datetime import UTC, datetime, timedelta
from http import HTTPStatus

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.repositories import UserRepository
from exceptions import AuthCredentialsError, AuthError
from settings import auth_settings
from utils.crypto import pwd_context
from utils.email import send_email
from utils.redis import get_verify_code, set_verify_code


class AuthUsecase:
    def __init__(self):
        self._user_repository = UserRepository()

    @staticmethod
    def _create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """Create an access token.

        Args:
            data: The data to encode.
            expires_delta: The expiration time.

        Returns:
            The access token.

        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(tz=UTC) + expires_delta
        else:
            expire = datetime.now(tz=UTC) + timedelta(
                minutes=auth_settings.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})

        return jwt.encode(
            claims=to_encode,
            key=auth_settings.secret_key,
            algorithm=auth_settings.algorithm,
        )

    def verify_token(self, token: str) -> dict:
        """Verify token and get payload.

        Args:
            token: The token.

        Returns:
            The payload.

        """
        try:
            return jwt.decode(
                token=token,
                key=auth_settings.secret_key,
                algorithms=[auth_settings.algorithm],
            )
        except JWTError as e:
            raise AuthCredentialsError from e

    @staticmethod
    def _generate_code() -> str:
        """Generate a code.

        Returns:
            The code.

        """
        return str(secrets.randbelow(900000) + 100000)

    async def _authenticate(
        self, session: AsyncSession, email: str, password: str
    ) -> User:
        """Authenticate a user.

        Args:
            session: The session.
            email: The email.
            password: The password.

        Returns:
            The user.

        """
        user = await self._user_repository.get_by(session=session, email=email)

        if not user or not user.is_active or not user.hashed_password:
            raise AuthCredentialsError

        if not pwd_context.verify(secret=password, hash=user.hashed_password):
            raise AuthCredentialsError

        return user

    async def _get_user_by_email(self, session: AsyncSession, email: str) -> User:
        """Get a user by email.

        Args:
            session: The session.
            email: The email.

        Returns:
            The user.

        """
        user = await self._user_repository.get_by(session=session, email=email)
        if not user:
            raise AuthError(
                message="User not found",
                status_code=HTTPStatus.NOT_FOUND,
            )

        return user

    async def get_current(self, session: AsyncSession, token: str) -> User:
        """Get the current user.

        Args:
            session: The session.
            token: The token.

        Returns:
            The current user.

        """
        email = self.verify_token(token=token).get("sub")

        if email is None:
            raise AuthCredentialsError

        user = await self._user_repository.get_by(session=session, email=email)

        if not user or not user.is_active:
            raise AuthCredentialsError

        return user

    async def login(self, session: AsyncSession, email: str, password: str) -> str:
        """Login a user.

        Args:
            session: The session.
            email: The email.
            password: The password.

        Returns:
            The token.

        """
        user = await self._authenticate(
            session=session,
            email=email,
            password=password,
        )

        if not user:
            raise AuthCredentialsError

        return self._create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=auth_settings.access_token_expire_minutes),
        )

    async def register(
        self,
        session: AsyncSession,
        email: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        """Register a user.

        Args:
            session: The session.
            email: The email.
            password: The password.
            first_name: The first name.
            last_name: The last name.

        Returns:
            The user.

        """
        if await self._user_repository.get_by(session=session, email=email):
            raise AuthError(
                message="Email already registered",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        return await self._user_repository.create(
            session=session,
            data={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "hashed_password": pwd_context.hash(secret=password),
                "is_active": False,
            },
        )

    async def send_email_code(self, session: AsyncSession, email: str) -> None:
        """Send an email code.

        Args:
            session: The session.
            email: The email.

        """
        user = await self._get_user_by_email(session=session, email=email)

        if user.is_active:
            raise AuthError(
                message="User is active",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        code = self._generate_code()
        await set_verify_code(identifier=user.email, code=code)

        html_content = (
            "<html><body><p>Code, which should be copied and used for "
            "authorization:</p><h3>{code}</h3><p>This message was sent by a robot, "
            "which does not check incoming mail</p></body></html>"
        ).format(code=code)

        send_email(
            email=user.email,
            html_content=html_content,
            subject="Your verification code",
        )

    async def verify_email(self, email: str, code: str, session: AsyncSession) -> None:
        """Verify an email.

        Args:
            email: The email.
            code: The code.
            session: The session.

        """
        user = await self._get_user_by_email(session=session, email=email)

        if user.is_active:
            raise AuthError(
                message="User is active",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        if await get_verify_code(identifier=user.email) != code:
            raise AuthError(
                message="Invalid code",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        await self._user_repository.update_by(
            session=session,
            data={"is_active": True},
            id=user.id,
        )
