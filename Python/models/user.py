class User:
    def __init__(self, **kwargs):
        self.username = kwargs.get('username', None)
        self.avatar_url = kwargs.get('avatar_url', None)
        self.gravatar_id = kwargs.get('gravatar_id', None)
        self.name = kwargs.get('name', None)
        self.company = kwargs.get('company', None)
        self.blog = kwargs.get('blog', None)
        self.location = kwargs.get('location', None)
        self.email = kwargs.get('email', None)
        self.bio = kwargs.get('bio', None)
        self.twitter_username = kwargs.get('twitter_username', None)
        self.hireable = kwargs.get('hireable', None)
