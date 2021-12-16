    ########################################################################
    ###########  METHODS FOR TOKEN AUTH ####################################
    ########################################################################
    # def get_token(self, exp=86400):
    #     current_time = dt.utcnow()
    #     #give the user their existing token in not exp.
    #     if self.token and self.token_exp > current_time + timedelta(seconds=60):
    #         return self.token
    #     #if expired or not exisitng, create new token and exp.
    #     self.token = secrets.token_urlsafe(32)
    #     self.token_exp = current_time + timedelta(seconds=exp)
    #     self.save()
    #     return self.token

    # def revoke_token (self):
    #     self.token_exp = dt.utcnow() - timedelta(seconds = 61)
    
    # @staticmethod
    # def check_token (token):
    #     u = User.query.filter_by(token = token).first()
    #     if not u or u.token_exp < dt.utcnow():
    #         return None
    #     return u

    ########################################################################
    ############  END METHODS FOR TOKENS  ##################################
    ########################################################################