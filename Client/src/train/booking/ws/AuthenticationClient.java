package train.booking.ws;

import java.rmi.RemoteException;
import train.booking.ws.AuthenticationStub.Login;
import train.booking.ws.AuthenticationStub.Logout;

public class AuthenticationClient
{
	public boolean login() throws RemoteException{
		AuthenticationStub hwp = new AuthenticationStub();
		Login s = new Login();
		s.setUsername("Moxim");
		s.setPassword("1234");
		System.out.print(hwp.login(s).get_return());
		return true;
	}
	
	public boolean logout() throws RemoteException{
		AuthenticationStub hwp = new AuthenticationStub();
		Logout s = new Logout();
		s.setUserId(1);
		System.out.print(hwp.logout(s).get_return());
		return true;
	}
	
	public boolean createAccount() throws RemoteException{
		return false;
	}

}
