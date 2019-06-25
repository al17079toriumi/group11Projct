package reportGeneratorApp;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Optional;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.scene.control.Alert;
import javafx.scene.control.Alert.AlertType;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.stage.FileChooser;

public class SaveController {
	String reportText = "";

	@FXML Label w4ReportContents;
    @FXML Button w4saveBtn;
    @FXML Button w4HomeBackBtn;
    @FXML Button w4FileChooserBackBtn;
    @FXML ScrollPane saveReportScroll;

	@FXML
    public void initialize() {
    	List<String> reportTextList = GenerateController.getReportTextList();
    	for(int i=0;i<GenerateController.getPathList().size();i++) {
    		if(i == GenerateController.getPathList().size()-1) {
        		reportText += reportTextList.get(i);
    		}else {
        		reportText += reportTextList.get(i)+"\n";
    		}
    	}
    	Label reportTextLabel = new Label(reportText);
    	saveReportScroll.setPadding(new Insets(10, 10, 10, 10));
    	saveReportScroll.setContent(reportTextLabel);
    }

	@FXML
	  public void saveReportAction(ActionEvent e) {
		 FileChooser fc = new FileChooser();
		 fc.setTitle("ファイル保存");
		 fc.setInitialDirectory(new File(System.getProperty("user.home")+"/Downloads"));
		 fc.setInitialFileName("report.txt");
		 File report = fc.showSaveDialog(null);
		 try {
			 if( report != null) {
				 BufferedWriter bw = new BufferedWriter(new FileWriter(report));
				 bw.write(reportText);
				 bw.close();
				 Alert savedAlrt = new Alert(AlertType.INFORMATION);
				 savedAlrt.setTitle("メッセージ");
				 savedAlrt.setHeaderText(null);
				 savedAlrt.setContentText("保存が完了しました");
				 savedAlrt.showAndWait();
				 new Main().changeView("w0.fxml");
			 }
		 }catch(IOException ex) {
			 Alert saveErrorAlert = new Alert(AlertType.ERROR);
			 saveErrorAlert.setTitle("エラー");
			 saveErrorAlert.setHeaderText("予期せぬエラーが発生しました。");
			 saveErrorAlert.setContentText("処理を中断します。");
			 saveErrorAlert.showAndWait();
		     System.out.println(ex);
		 }
	}

	@FXML
    public void backFromW4ToW0(ActionEvent e) {
		if(backAlartFunc()) {
	        new Main().changeView("w0.fxml");
		}
    }
	@FXML
    public void backFromW4ToW3(ActionEvent e) {
		if(backAlartFunc()) {
	        new Main().changeView("w3.fxml");
		}
	}
	public boolean backAlartFunc() {
		Alert backAlert = new Alert(AlertType.CONFIRMATION);
		backAlert.setTitle("ナビゲーションの確認");
		backAlert.setHeaderText("生成したレポートの保存が完了していません。");
		backAlert.setContentText("このページから移動してもよろしいですか？");

		Optional<ButtonType> result = backAlert.showAndWait();
		if (result.get() == ButtonType.OK){
			return true;
		}else {
			return false;
		}
	}
}
