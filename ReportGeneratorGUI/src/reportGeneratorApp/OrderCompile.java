package reportGeneratorApp;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class OrderCompile {
	public static String compile(String sourceFilePath) {

		String path = System.getProperty("user.dir");
		String compileText = "";

		List<String> cmdCpl = new ArrayList<String>(Arrays.asList("script","-q","compile.log","gcc", sourceFilePath, "-o", path+"/a.out"));
		List<String> cmdRm = new ArrayList<String>(Arrays.asList("rm",path+"/compile.log"));
		Process p1 = null;
		Process p2 = null;
		try {
			ProcessBuilder pb1 = new ProcessBuilder(cmdCpl);
			ProcessBuilder pb2 = new ProcessBuilder(cmdRm);

			p1 = pb1.start();
            p1.waitFor();

            File logFile = new File(path + "/compile.log");
            BufferedReader br = new BufferedReader(new FileReader(logFile));
            String logLine;
            while((logLine = br.readLine()) != null) {
            	compileText += logLine+"\n";
            }
            br.close();

            p2 = pb2.start();
            p2.waitFor();

        	return compileText;
		} catch (InterruptedException | IOException e){
            e.printStackTrace();
            compileText = "Erroer by Application";
        	return compileText;
        }
	}
}
