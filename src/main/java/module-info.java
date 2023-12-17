module de.agb.restapifruitshop {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;
    requires com.dlsc.formsfx;
    requires com.fasterxml.jackson.databind;

    opens de.agb.restapifruitshop to javafx.fxml;
    exports de.agb.restapifruitshop;
}