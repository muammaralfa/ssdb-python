from pydantic import BaseSettings


class Config(BaseSettings):
    BEANSTALK_HOST: str
    BEANSTALK_PORT: int
    SSDB_HOST: str
    SSDB_PORT: str
    TUBE: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


app_setting = Config()
