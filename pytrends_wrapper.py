class googleTrends():
    def __init__(self, conf):
        self.conf = conf

        self.countries_dict = {
            'Guatemala':'GT', 
            'Colombia':'CO', 
            'Spain':'ES', 
            'Mexico':'MX', 
            'Canada':'CA', 
            'India':'IN',
            'Venezuela, RB':'VE', 
            'Argentina':'AR', 
            'United States':'US', 
            'Chile':'CL', 
            'Peru':'PE',
            'Ecuador':'EC', 
            'Cameroon':'CM', 
            'United Kingdom':'GB', 
            'Ireland':'IE', 
            'Australia':'AT',
            'RSA':'ZA', 
            'Philippines':'PH', 
            'Czechia':'CZ',
            'Luxembourg':'LU'
        }
        '''
        #self.countries_dict = {key: countries[key] for key in self.conf['countries']}
        '''
        self.world_panel = self.get_world_panel()
        
    def get_world_panel(self):
        '''
        Returns world panel data
        '''
        world_data = self.get_regional_data(
            resolution = 'COUNTRY',
            start_date=self.conf['start_date'],
            end_date=self.conf['end_date'],
            key_word=self.conf['ggt_key_word'],
            state=None
        )
        wdata = {}
        searches = {}
        for geo in world_data.iterrows():
            if geo[1]['geoCode'] in self.countries_dict.values():
                searches[geo[1]['geoCode']] = self.get_searches(
                    key_word=self.conf['ggt_key_word'],
                    state=geo[1]['geoCode'],
                    region=None,
                    start_date=self.conf['start_date'],
                    end_date=self.conf['end_date']
                )
                wdata[geo[1]['geoCode']] = geo[1][self.conf['ggt_key_word']]
        toret = self.bilateral_adjust(searches, wdata)
        toret = self.build_df(toret)
        return(toret)
    
    def get_regional_panel(self):
        '''
        Returns regional panel data for a given country.
        '''
        regional_data = self.get_regional_data(
            resolution = 'REGION',
            start_date=self.conf['start_date'],
            end_date=self.conf['end_date'],
            key_word=self.conf['ggt_key_word'],
            state=self.conf['ggt_state']
        )
        return(regional_data)
    
    
    def get_regional_data(self, resolution, start_date, end_date, key_word, state):
        '''
        Returns temporal average result for all the world countries.
        '''
        pytrends = TrendReq()
        pytrends.build_payload([key_word], 
                        cat=0, 
                        timeframe='{} {}'.format(start_date, end_date),  
                        gprop='',geo=state) 
        df =pytrends.interest_by_region(resolution=resolution, 
                                        inc_low_vol=True, 
                                        inc_geo_code=True)
        return(df)

    def get_searches(self, key_word, state, region, start_date, end_date):
        '''
        Returns temporal result for a unic individual.
        '''
        if region != None:
            geo = '{}-{}'.format(state,region)
        else:
            geo = state
            
        pytrends = TrendReq()
        pytrends.build_payload([key_word], 
                               cat=0, 
                               timeframe='{} {}'.format(start_date, end_date),  
                               gprop='',geo=geo)    
        df = pytrends.interest_over_time()
        return(df)
    
    def bilateral_adjust(self, searches, wdata):
        '''
        Calculates the bilateral adjust between corss section following IMF
        working paper appendix procedure.
        '''
        reference = max(wdata.items(), key=operator.itemgetter(1))
        for code in wdata.keys():
            coef = ((wdata[code]/ # temporal mean of given country
                     searches[code][self.conf['ggt_key_word']].mean())* # mean of the temporal series of given country
                    (searches[reference[0]][self.conf['ggt_key_word']].mean()/ # mean of the temporal series of reference country
                     reference[1])) # temporal mean of the reference country
            searches[code]['adjusted_index']=searches[code][self.conf['ggt_key_word']]*coef
        return(searches)
    
    def build_df(self, searches):
        '''
        BUilds final df result from dict.
        '''
        toret = pd.DataFrame()
        for df in searches.items():
            matrix = df[1]
            matrix['countryCode'] = df[0]
            toret = toret.append(matrix)
        return(toret)
