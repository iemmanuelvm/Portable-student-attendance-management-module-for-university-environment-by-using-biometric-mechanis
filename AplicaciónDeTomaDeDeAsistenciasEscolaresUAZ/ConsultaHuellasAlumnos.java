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
class ConsultaHuellasAlumnos {
	public static void main( String[] args ) throws IOException, Exception {
		File miDir = new File (".");
		String cadena;
		String c="";
	        FileReader f = new FileReader(miDir.getCanonicalPath()+"/CONFIGURACION_DB/conexiondb.uaz");
	        BufferedReader b = new BufferedReader(f);
	        while((cadena = b.readLine())!=null) {
			c = cadena;
	      	}
	      	b.close();
		byte[] decodedBytes = Base64.getDecoder().decode(c);
		String decodedString = new String(decodedBytes);
		String[] parts = decodedString.split("\n");
		int day = Integer.parseInt(args[0]);
		
		String claDoc = args[1];
		
		String CE = args[2];
		
        	switch(day) 
        	{
            	case 1:  
			Huellas("GH.GH_LUNESINI",claDoc,CE,parts[0],parts[1],parts[2],parts[3],parts[4]);
                     	break;
		case 2:  
			Huellas("GH.GH_MARTESINI",claDoc,CE,parts[0],parts[1],parts[2],parts[3],parts[4]);
                     	break;
		case 3:  
			Huellas("GH.GH_MIERCOLESINI",claDoc,CE,parts[0],parts[1],parts[2],parts[3],parts[4]);
                     	break;
		case 4:  
			Huellas("GH.GH_JUEVESINI",claDoc,CE,parts[0],parts[1],parts[2],parts[3],parts[4]);
                     	break;
		case 5:  
			Huellas("GH.GH_VIERNESINI",claDoc,CE,parts[0],parts[1],parts[2],parts[3],parts[4]);
                     	break;
		case 6:  
			Huellas("GH.GH_SABADOINI",claDoc,CE,parts[0],parts[1],parts[2],parts[3],parts[4]);
                     	break;
            	default: 
                     break;
        	}
        }
	public static void Huellas(String dia, String docente, String ce, String user, String pass, String IP, String db, String Puerto) throws IOException, Exception 
	{
		String url = "jdbc:oracle:thin:@"+IP+":"+Puerto+":"+db;
  		String username = user;
  		String password = pass;
    		Class.forName("oracle.jdbc.driver.OracleDriver");
    		Connection conn = DriverManager.getConnection(url, username, password);
		String sql = "SELECT AL.AL_MATRICULA, AL.AL_HUELLA FROM ALUMNO AL JOIN ASIGNATURA ASI ON ASI.AL_MATRICULA = AL.AL_MATRICULA JOIN GRUPO GR ON ASI.GR_CLAVE = GR.GR_CLAVE JOIN MATERIA MA ON MA.MT_CLAVE = GR.MT_CLAVE JOIN GRUPO_HORARIO GH ON GH.GR_CLAVE = GR.GR_CLAVE WHERE GR.CE_CLAVE = '"+ce+"' AND "+dia+" IS NOT NULL AND GR.DO_CLAVE = '"+docente+"' ORDER BY MA.MT_CLAVE";
			PreparedStatement stmt = conn.prepareStatement(sql);
			ResultSet resultSet = stmt.executeQuery(sql);
			while (resultSet.next()) {
      			try {
				if(resultSet.getBinaryStream(2)!=null)
				{
				File miDir = new File (".");
             			String name = resultSet.getString(1).replace(" ","");
     				File image = new File(miDir.getCanonicalPath()+"/HUELLAS/"+name);
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
		System.out.println("TRUE-HUELLAS-ALUMNOS");
	}
}

