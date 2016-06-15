package org.openstreetmap.josm.plugins.pt_assistant.gui;

import static org.openstreetmap.josm.tools.I18n.tr;

import java.awt.Component;

import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JCheckBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.SwingUtilities;

public class ProceedDialog extends JPanel {

	private static final long serialVersionUID = 2986537034076698693L;

	private enum ASK_TO_PROCEED {
		DO_ASK, DONT_ASK_AND_FIX_AUTOMATICALLY, DONT_ASK_AND_FIX_MANUALLY, DONT_ASK_AND_DONT_FIX
	};

	// by default, the user should be asked
	private static ASK_TO_PROCEED askToProceed = ASK_TO_PROCEED.DO_ASK;

	private JRadioButton radioButtonFixAutomatically;
	private JRadioButton radioButtonFixManually;
	private JRadioButton radioButtonDontFix;
	private JCheckBox checkbox;
	private String[] options;
	private JPanel panel;
	private int selectedOption;

	public ProceedDialog(long id, int numberOfDirectionErrors, int numberOfRoadTypeErrors) {

		panel = new JPanel();
		panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));

		JLabel label1 = new JLabel(tr("PT_Assistant plugin found that this relation (id=" + id + ") has errors:"));
		panel.add(label1);
		label1.setAlignmentX(Component.LEFT_ALIGNMENT);

		if (numberOfDirectionErrors != 0) {
			JLabel label2 = new JLabel("     " + numberOfDirectionErrors + tr(" direction errors"));
			panel.add(label2);
			label2.setAlignmentX(Component.LEFT_ALIGNMENT);
		}

		if (numberOfRoadTypeErrors != 0) {
			JLabel label3 = new JLabel("     " + numberOfRoadTypeErrors + tr(" road type errors"));
			panel.add(label3);
			label3.setAlignmentX(Component.LEFT_ALIGNMENT);
		}

		JLabel label4 = new JLabel(tr("How do you want to proceed?"));
		panel.add(label4);
		label4.setAlignmentX(Component.LEFT_ALIGNMENT);

		radioButtonFixAutomatically = new JRadioButton("Fix all errors automatically and proceed", true);
		radioButtonFixManually = new JRadioButton("I will fix the erros manually and click the button to proceed");
		radioButtonDontFix = new JRadioButton("Do not fix anything and proceed with further tests");
		ButtonGroup fixOptionButtonGroup = new ButtonGroup();
		fixOptionButtonGroup.add(radioButtonFixAutomatically);
		fixOptionButtonGroup.add(radioButtonFixManually);
		fixOptionButtonGroup.add(radioButtonDontFix);
		panel.add(radioButtonFixAutomatically);
		panel.add(radioButtonFixManually);
		panel.add(radioButtonDontFix);
		radioButtonFixAutomatically.setAlignmentX(Component.LEFT_ALIGNMENT);
		radioButtonFixManually.setAlignmentX(Component.LEFT_ALIGNMENT);
		radioButtonDontFix.setAlignmentX(Component.LEFT_ALIGNMENT);

		checkbox = new JCheckBox(tr("Remember my choice and don't ask me again in this session"));
		panel.add(checkbox);
		checkbox.setAlignmentX(Component.LEFT_ALIGNMENT);

		options = new String[2];
		options[0] = "OK";
		options[1] = "Cancel & stop testing";

		selectedOption = Integer.MIN_VALUE;

	}

	/**
	 * Finds out whether the user wants to download incomplete members. In the
	 * default case, creates a JOptionPane to ask.
	 * 
	 * @return 0 to fix automatically, 1 to fix manually, 2 to proceed without
	 *         fixing, -1 to stop testing or if dialog is closed without answer
	 * 
	 */
	public int getUserSelection() {

		if (askToProceed == ASK_TO_PROCEED.DONT_ASK_AND_FIX_AUTOMATICALLY) {
			return 0;
		}
		if (askToProceed == ASK_TO_PROCEED.DONT_ASK_AND_FIX_MANUALLY) {
			return 1;
		}
		if (askToProceed == ASK_TO_PROCEED.DONT_ASK_AND_DONT_FIX) {
			return 2;
		}

		// showDialog(); FIXME
		selectedOption = JOptionPane.showOptionDialog(this, panel, tr("PT_Assistant Proceed Request"),
				JOptionPane.DEFAULT_OPTION, JOptionPane.QUESTION_MESSAGE, null, options, 0);

		if (selectedOption == 0) {
			if (radioButtonFixAutomatically.isSelected()) {
				if (checkbox.isSelected()) {
					askToProceed = ASK_TO_PROCEED.DONT_ASK_AND_FIX_AUTOMATICALLY;
				}
				return 0;
			}
			if (radioButtonFixManually.isSelected()) {
				if (checkbox.isSelected()) {
					askToProceed = ASK_TO_PROCEED.DONT_ASK_AND_FIX_MANUALLY;
				}
				return 1;
			}
			if (radioButtonDontFix.isSelected()) {
				if (checkbox.isSelected()) {
					askToProceed = ASK_TO_PROCEED.DONT_ASK_AND_DONT_FIX;
				}
				return 2;
			}
		}

		return -1;
	}

	/**
	 * 
	 */
	private void showDialog() {

		if (!SwingUtilities.isEventDispatchThread()) {
			selectedOption = JOptionPane.showOptionDialog(this, panel, tr("PT_Assistant Proceed Request"),
					JOptionPane.DEFAULT_OPTION, JOptionPane.QUESTION_MESSAGE, null, options, 0);
		} else {

			SwingUtilities.invokeLater(new Runnable() {
				@Override
				public void run() {
					showDialog();
				}
			});

		}

	}

}
