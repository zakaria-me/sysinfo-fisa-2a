package train.booking.ws;

import java.rmi.RemoteException;
import java.util.Scanner;


public class Main {

	public static void main(String[] args) {
		boolean authenticated = false;
		Scanner scan = new Scanner(System.in);
		printActionChoices(authenticated);
		// Scan user choice while it's not an integer
		while(!scan.hasNextInt()) {
			System.out.println("Veuillez entrer un nombre valide");
			System.out.print("t>");
			scan.next();
		}
		int choice = scan.nextInt();
		System.out.println("Vous avez choisi : " + choice);
		if(authenticated) {
			runAuthenticatedAction(choice);
		}else {
			runUnauthenticatedAction(choice, scan);
		}
	}
	
	public static void printActionChoices(boolean authenticated) {
		System.out.println("\tQuelle action voulez vous effectuer ?");
		if(authenticated) {
			System.out.println("\t\t1 - Consulter les trains");
			System.out.println("\t\t2 - Faire une réservation");
		}else {
			System.out.println("\t\t1 - Se connecter");
			System.out.println("\t\t2 - Créer un compte");
		}
		System.out.println("\t\t0 - Quitter");
		System.out.print("\t>");
	}
	
	public static void runAuthenticatedAction(int action) {
		if(action == 0) {
			System.out.println("Ciao bye !");
			// Logout
			System.exit(0);
		}
		if(action == 1) {
			System.out.println("\t\t1 - Consulter les trains");
		}else {
			System.out.println("\t\t2 - Faire une réservation");
		}
	}
	
	public static void runUnauthenticatedAction(int action, Scanner scan) {
		if(action == 0) {
			System.out.println("Ciao bye !");
			System.exit(0);
		}
		AuthenticationClient authClient = new AuthenticationClient();
		System.out.println("\t\tUsername : ");
		String username = scan.next();
		System.out.println("\t\tPassword : ");
		String password = scan.next();
		try {
			if(action == 1) {
				authClient.login(username, password);
			}else {
				authClient.createAccount(username, password);
			}
		}catch(RemoteException e){
			System.out.println("ERROR");
		}
	}

}
