import booking_details as script

#############################################
############# BOOKING DETAILS ###############
#############################################

class TestBookingDetails:
    BOOKINGDETAILS = script.BookingDetails(destination='Berlin', origin='Poznan', budget='280', travel_date='09/03/2022', return_date='10/03/2022')

    # Booking details
    # - Modifier un attribut destination
    def test_set_destination(self):
        self.BOOKINGDETAILS.destination = 'Strasbourg'
        assert self.BOOKINGDETAILS.destination == 'Strasbourg'
    
    # - Modifier un attribut origin
    def test_set_origin(self):
        self.BOOKINGDETAILS.origin = 'Paris'
        assert self.BOOKINGDETAILS.origin == 'Paris'

    # - Modifier un attribut budget
    def test_set_budget(self):
        self.BOOKINGDETAILS.budget = '250'
        assert self.BOOKINGDETAILS.budget == '250'
    
    # - Modifier un attribut budget
    def test_set_travel_date(self):
        self.BOOKINGDETAILS.travel_date = '07/03/2022'
        assert self.BOOKINGDETAILS.travel_date == '07/03/2022'

    # - Modifier un attribut budget
    def test_set_return_date(self):
        self.BOOKINGDETAILS.return_date = '08/03/2022'
        assert self.BOOKINGDETAILS.return_date == '08/03/2022'

    # - Récupérer un attribut destination
    def test_get_destination(self):
        assert self.BOOKINGDETAILS.destination == 'Strasbourg'
    
    # - Récupérer un attribut origin
    def test_get_origin(self):
        assert self.BOOKINGDETAILS.origin == 'Paris'

    # - Récupérer un attribut budget
    def test_get_budget(self):
        assert self.BOOKINGDETAILS.budget == '250'

    # - Récupérer un attribut travel_date
    def test_get_travel_date(self):
        assert self.BOOKINGDETAILS.travel_date == '07/03/2022'

    # - Récupérer un attribut return_date
    def test_get_return_date(self):
        assert self.BOOKINGDETAILS.return_date == '08/03/2022'