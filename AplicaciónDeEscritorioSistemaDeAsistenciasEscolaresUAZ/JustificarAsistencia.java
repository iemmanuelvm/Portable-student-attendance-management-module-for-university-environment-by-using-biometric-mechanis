import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

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

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.io.*;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.IOException;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Base64;
//escolar$-#escolar123_$-#148.217.200.133$-#orcl$-#1521
class JustificarAsistencia {
	public static void main( String[] args ) throws IOException, Exception, SQLException {
		String aux = "";
		File miDir = new File (".");
        	try {
            		Scanner input = new Scanner(new File(miDir.getCanonicalPath()+"/auxHuella/docente.uaz"));
            		while (input.hasNextLine()) {
                		String line = input.nextLine();
				aux = line;
            		}
            		input.close();
        	} catch (Exception ex) {
            		ex.printStackTrace();
        	}
		String[] parts = aux.split("\\+");

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

		String url = "jdbc:oracle:thin:@"+parts1[2]+":"+parts1[4]+":"+parts1[3];
  		String username = parts1[0];
  		String password = parts1[1];
    		Class.forName("oracle.jdbc.driver.OracleDriver");
    		Connection conn = DriverManager.getConnection(url, username, password);
		String sql = "SELECT AL.AL_MATRICULA, AL.AL_HUELLA FROM ALUMNO AL JOIN ASIGNATURA ASI ON AL.AL_MATRICULA = ASI.AL_MATRICULA JOIN GRUPO GR ON GR.GR_CLAVE = ASI.GR_CLAVE AND GR.DO_CLAVE = '"+parts[0]+"'";
			PreparedStatement stmt = conn.prepareStatement(sql);
			ResultSet resultSet = stmt.executeQuery(sql);
			
			while (resultSet.next()) {
      			try {
				
				if(resultSet.getBinaryStream(2)!=null)
				{
		     			String name = resultSet.getString(1).replace(" ","");
	     				File image = new File(miDir.getCanonicalPath()+"/auxHuella/JUSTIFICACIONES/"+name);
					FileOutputStream fos = new FileOutputStream(image);
					
	      				byte[] buffer = new byte[1];
	      				InputStream is = resultSet.getBinaryStream(2);
	      				while (is.read(buffer) > 0) {
						fos.write(buffer);
	      				}
	      				fos.close();
				}
       			}
     			catch(Exception e) {
       			e.printStackTrace();
       			}
    		}
		conn.close();
        }
}

