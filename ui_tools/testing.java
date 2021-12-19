import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

class testing implements KeyListener {
    double lastPress = 0;

    public static void main(String[] args) {
        Frame f = new Frame("yes");
        f.addKeyListener(new testing());
        f.setVisible(true);
    }

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        double newPress = System.currentTimeMillis();
        System.out.println(newPress - lastPress);
        lastPress = newPress;
    }

    @Override
    public void keyReleased(KeyEvent e) {

    }
}