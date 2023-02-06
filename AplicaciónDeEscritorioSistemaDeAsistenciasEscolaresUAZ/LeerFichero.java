import java.io.File;
import java.util.Scanner;
import java.lang.Object;
import java.util.Base64;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import oracle.jdbc.driver.OracleDriver;
import java.lang.Object;
import java.lang.Throwable;
import java.lang.Exception;
import java.sql.SQLException;
import java.io.FileInputStream;

public class LeerFichero {
	public static void main(String[] args) throws SQLException {
		String aux = "";
		File miDir = new File (".");
        	try {
            		Scanner input = new Scanner(new File(miDir.getCanonicalPath()+"/auxHuella/datos.uaz"));
            		while (input.hasNextLine()) {
                		String line = input.nextLine();
				aux = line;
            		}
            		input.close();
        	} catch (Exception ex) {
            		ex.printStackTrace();
        	}
		byte[] decodedBytes = Base64.getDecoder().decode(aux);
		String decodedString = new String(decodedBytes);
		String[] parts = decodedString.split(",");


		String aux1 = "";
		File miDir1 = new File (".");
        	try {
            		Scanner input1 = new Scanner(new File(miDir1.getCanonicalPath()+"/auxHuella/conexiondb.uaz"));
            		while (input1.hasNextLine()) {
                		String line1 = input1.nextLine();
				aux1 = line1;
            		}
            		input1.close();
        	} catch (Exception ex) {
            		ex.printStackTrace();
        	}




		byte[] decodedBytes1 = Base64.getDecoder().decode(aux1);
		String decodedString1 = new String(decodedBytes1);
		String[] parts1 = decodedString1.split("-");
		try {
            		DriverManager.registerDriver(new OracleDriver());
	    		String NombreServidor = parts1[2];
           	 	String NumeroPuerto = parts1[4];
            		String Sid = parts1[3];
	    		String User = parts1[0];
            		String Pass = parts1[1];
	    		String URL = "jdbc:oracle:thin:@" + NombreServidor + ":" + NumeroPuerto + ":" + Sid;
            		Connection AbrirConexion = DriverManager.getConnection(URL, User, Pass);
            		PreparedStatement guardarStmt = 
            		AbrirConexion.prepareStatement("INSERT INTO ALUMNO(AL_MATRICULA,AL_APATERNO,AL_AMATERNO,AL_NOMBRE,AL_FECHANAC,AL_CALLE,AL_COLONIA,AL_CP,AL_TELEFONO,AL_EMAIL,AL_GENERO,AL_STATUS,AL_EXTRANJERO,AL_MUNICIPIO,AL_ESTADO,AL_FINGRESO,AL_HUELLA,AL_VOZ) VALUES(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18)");
	    		for (int i = 0 ; i < parts.length ; i++) {
				if(parts[i].equals("NULL"))
				{
					guardarStmt.setString((i+1),"");
				}
            			else
				{
					guardarStmt.setString((i+1), parts[i]);	
				}
            		}
			try {
			  	File picfile = new File(miDir.getCanonicalPath()+"/auxHuella/HUELLA/huella"+parts[0]);
	    			FileInputStream fis = new FileInputStream(picfile);
	    			guardarStmt.setBinaryStream(17, fis, (int) picfile.length());
			}
			catch(Exception e) {
			  	guardarStmt.setNull(17, java.sql.Types.BLOB);
			}
			try {
			  	File picfile = new File(miDir.getCanonicalPath()+"/MuestrasDeVoz/ModeloGMM/voz"+parts[0]+".gmm");
	    			FileInputStream fis = new FileInputStream(picfile);
	    			guardarStmt.setBinaryStream(18, fis, (int) picfile.length());
			}
			catch(Exception e) {
			  	guardarStmt.setNull(18, java.sql.Types.BLOB);
			}
	    		
            		guardarStmt.execute();
          	}
          	catch (Exception e) {
	    		System.out.println("Ocurrio un error inesperado");
            		e.printStackTrace();
          	}
	
    	}
}
