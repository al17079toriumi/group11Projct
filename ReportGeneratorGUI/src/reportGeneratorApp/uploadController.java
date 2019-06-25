package reportGeneratorApp;

import javafx.fxml.FXML;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;

public class uploadController {

	@FXML WebView upload;
	public void initialize() {
		WebEngine engine = upload.getEngine();
		engine.load("https://www.google.co.jp/");
	}
}
