package reportGeneratorApp;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;

public class Controller {

	 @FXML Button w0LogInBtn;
	 @FXML Button w0FileSeiseiBtn;

	 @FXML
	    public void changeFromW0ToW3(ActionEvent e) {
	        new Main().changeView("w3.fxml");
	    }
	 @FXML
	    public void changeFromW0ToRU(ActionEvent e) {
	        new Main().changeView("reportUpload.fxml");
	    }
}
