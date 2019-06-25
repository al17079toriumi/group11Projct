package reportGeneratorApp;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class GenerateReport {
	public static String generateReport(String sourceFilePath,String kadaiNum,String claText) {
		String reportText = "", resultText = "", sourceText = "";
		String[] claTexts = claText.split(" ");
		String path = System.getProperty("user.dir");

		try {
			File shFile = new File(path + "/cla.sh");
			BufferedWriter bw = new BufferedWriter(new FileWriter(shFile));

			bw.write("#!/usr/bin/env bash");
	        bw.newLine();
	        bw.write("cd `dirname $0`");
	        bw.newLine();
	        bw.write("sh excution.sh ");
	        for(int i=0;i<claTexts.length;i++) {
				bw.write(claTexts[i] + " ");
			}
	        bw.newLine();
            bw.close();
		}catch(IOException e){
		      System.out.println(e);
		      return "Erroer by Application";
	    }

		List<String> cmdChmod = new ArrayList<String>(Arrays.asList("chmod","+x","cla.sh"));
		List<String> cmdExcution = new ArrayList<String>(Arrays.asList("open","-W","-a","terminal",path+"/cla.sh"));
		List<String> cmdCat = new ArrayList<String>(Arrays.asList("cat",sourceFilePath));
		List<String> cmdRm = new ArrayList<String>(Arrays.asList("rm",path+"/output.log"));

        try {
            ProcessBuilder pb1 = new ProcessBuilder(cmdChmod);
            ProcessBuilder pb2 = new ProcessBuilder(cmdExcution);
            ProcessBuilder pb3 = new ProcessBuilder(cmdCat);
            ProcessBuilder pb4 = new ProcessBuilder(cmdRm);

            Process p1 = pb1.start();
            p1.waitFor();
            Process p2 = pb2.start();
            p2.waitFor();
            Process p3 = pb3.start();
            p3.waitFor();

            InputStream is = p3.getInputStream();
	        BufferedReader br = new BufferedReader(new InputStreamReader(is));
	        String sourceLine;
            while ((sourceLine = br.readLine()) != null) {
            	 sourceText += sourceLine+"\n";
            }
            br.close();

            File logFile = new File(path + "/output.log");
            BufferedReader br2 = new BufferedReader(new FileReader(logFile));
            String logLine;
            while((logLine = br2.readLine()) != null) {
            	resultText += logLine+"\n";
            }
            br2.close();

            Process p4 = pb4.start();
            p4.waitFor();
        }catch (IOException | InterruptedException e){
            e.printStackTrace();
            return "Erroer by Application";
		}

        reportText += "課題"+kadaiNum+"\n\n";
        reportText += "ソースコード\n";
        reportText += sourceText+"\n";
        reportText += "実行結果\n";
        reportText += resultText;

        return reportText;
	}
}
