from app_test.config.env_config import EnvConfig

default_env = "DEV_DEFAULT"


def env_api_url(envSetup):
    print("envSetup::::::::::::::::::::::", envSetup)
    try:
        env = EnvConfig.ApiEnv(envSetup)
        print("ENV.URL", env.URL)
        return env.URL
    except:
        env = EnvConfig.ApiEnv(default_env)
        print("ENV.URL", env.URL)
        return env.URL


def env_app_url(envSetup):
    print("envSetup::::::::::::::::::::::", envSetup)
    try:
        env = EnvConfig.ApplicationEnv(envSetup)
        print("ENV.URL", env.URL)
        return env.URL
    except:
        env = EnvConfig.ApplicationEnv(default_env)
        print("ENV.URL", env.URL)
        return env.URL
