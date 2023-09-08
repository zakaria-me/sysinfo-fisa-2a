package train.booking.ws;

import java.time.LocalDateTime;

public class FirstSoap {
	
	public String sayHello(String input){
		return "Hello "+input;
	}
	
	public void getTrains(
			String departureStation, String arrivalStation,
			LocalDateTime outbound, LocalDateTime returnDate,
			int nbTickets, int travelClass){
		
	}
}
