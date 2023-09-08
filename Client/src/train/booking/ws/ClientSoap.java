package train.booking.ws;

import java.rmi.RemoteException;
import train.booking.ws.FirstSoapStub.SayHello;

public class ClientSoap {
	/**
	 * @param args
	 * @throws RemoteException 
	 */
	public static void main(String[] args) throws RemoteException {
		// TODO Auto-generated method stub
		FirstSoapStub hwp = new FirstSoapStub();
		SayHello s = new SayHello();
		s.setInput("from client");
		System.out.print(hwp.sayHello(s).get_return());
	}

}
