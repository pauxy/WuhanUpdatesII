class Country:
    name = None
    update = None
    latlong = None
    confirmed = None
    death = None
    recovered = None
    active = None
    incident = None
    mortality = None

    def __init__(self, name, update, latlong, confirmed, death, recovered, active, incident,
                 mortality):
        self.name = name
        self.update = update
        self.latlong = latlong
        self.confirmed = confirmed
        self.death = death
        self.recovered = recovered
        self.active = active
        self.incident = incident
        self.mortality = mortality

    def beautify(self):
        beautified = "Name : {0}\n\
Last Updated : {1}\n\
Lat Long : {2}\n\
Confirmed cases : {3}\n\
Deaths : {4}\n\
Recovered : {5}\n\
Active Cases : {6}\n\
Mortality Rate : {7}%\n".format(self.name, self.update, self.latlong, self.confirmed, self.death,
                                self.recovered, self.active, self.mortality)
        return beautified
    
    def listoutput(self,comparison):
        return "{0}     -     {1}\n".format(self.name,str(round(comparison,3)))
