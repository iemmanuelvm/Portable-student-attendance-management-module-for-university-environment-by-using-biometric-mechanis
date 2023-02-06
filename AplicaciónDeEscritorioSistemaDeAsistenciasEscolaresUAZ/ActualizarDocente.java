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

public class ActualizarDocente {
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
         		//AL_MATRICULA,AL_APATERNO,AL_AMATERNO,AL_NOMBRE,AL_FECHANAC,AL_CALLE,AL_COLONIA,AL_CP,AL_TELEFONO,AL_EMAIL,AL_GENERO,AL_STATUS,AL_EXTRANJERO,AL_MUNICIPIO,AL_ESTADO,AL_FINGRESO,AL_HUELLA,AL_VOZ
			//DO_CLAVE,GE_CLAVE,DO_APATERNO,DO_AMATERNO,DO_NOMBRE,DO_FECHANAC,DO_CALLE,DO_COLONIA,DO_CP,DO_TELEFONO,DO_TELCELL,DO_EMAIL,DO_TITULO,DO_GENERO,DO_HUELLA,DO_VOZ	
			//1111,3,BECERRA,SANCHEZ,ALDONSO,31/Mayo/1985,velino,vega,98835,49612547,778787,z,1,z		
			PreparedStatement guardarStmt = 
            		AbrirConexion.prepareStatement("UPDATE DOCENTE SET GE_CLAVE = :1, DO_APATERNO = :2, DO_AMATERNO = :3,  DO_NOMBRE = :4,  DO_FECHANAC = :5,  DO_CALLE = :6,  DO_COLONIA = :7,  DO_CP = :8,  DO_TELEFONO = :9, DO_TELCELL = :10, DO_EMAIL = :11,  DO_GENERO = :12,   DO_TITULO = :13 WHERE DO_CLAVE = :14");

			for (int i = 1 ; i < parts.length ; i++) {
				if(parts[i].equals("NULL"))
				{
					guardarStmt.setString((i),"");
				}
            			else
				{
					guardarStmt.setString((i), parts[i]);	
				}
            		}

			
			guardarStmt.setString(14, parts[0]);
			guardarStmt.execute();
			
			File picfile = new File(miDir.getCanonicalPath()+"/auxHuella/HUELLA/huella"+parts[0]);

			if (!picfile.exists()) {
		    		
			}
	    		else{
				PreparedStatement guardarStmtq = 
		    		AbrirConexion.prepareStatement("UPDATE DOCENTE SET DO_HUELLA = :15 WHERE DO_CLAVE = :1");
				FileInputStream fis = new FileInputStream(picfile);
		    		guardarStmtq.setBinaryStream(1, fis, (int) picfile.length());
				guardarStmtq.setString(2, parts[0]);
				guardarStmtq.execute();
			}
			
			File picfile1 = new File(miDir.getCanonicalPath()+"/MuestrasDeVoz/ModeloGMM/voz"+parts[0]+".gmm");
			
			if (!picfile1.exists()) {
		    		
			}
	    		else{
				PreparedStatement guardarStmtq = 
		    		AbrirConexion.prepareStatement("UPDATE DOCENTE SET DO_VOZ = :16 WHERE DO_CLAVE = :1");
				FileInputStream fis = new FileInputStream(picfile1);
		    		guardarStmtq.setBinaryStream(1, fis, (int) picfile1.length());
				guardarStmtq.setString(2, parts[0]);
				guardarStmtq.execute();
			}
          	}
          	catch (Exception e) {
	    		System.out.println("Ocurrio un error inesperado");
            		e.printStackTrace();
          	}
		
	
    	}
}
