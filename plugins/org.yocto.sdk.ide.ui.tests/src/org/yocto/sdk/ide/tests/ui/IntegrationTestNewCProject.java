package org.yocto.sdk.ide.tests.ui;

import static org.junit.Assert.assertTrue;

import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Control;
import org.eclipse.swt.widgets.Tree;
import org.eclipse.swtbot.eclipse.finder.SWTWorkbenchBot;
import org.eclipse.swtbot.eclipse.finder.widgets.SWTBotView;
import org.eclipse.swtbot.swt.finder.junit.SWTBotJunit4ClassRunner;
import org.eclipse.swtbot.swt.finder.matchers.WidgetMatcherFactory;
import org.eclipse.swtbot.swt.finder.widgets.SWTBotShell;
import org.eclipse.swtbot.swt.finder.widgets.SWTBotTable;
import org.eclipse.swtbot.swt.finder.widgets.SWTBotTableItem;
import org.eclipse.swtbot.swt.finder.widgets.SWTBotTree;
import org.eclipse.swtbot.swt.finder.widgets.SWTBotTreeItem;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;

/* FIXME: ALL strings should be internationalized */

@RunWith(SWTBotJunit4ClassRunner.class)
public class IntegrationTestNewCProject {
	
	private static SWTWorkbenchBot bot;
	
	/* Use unique project names for each type that is to be tested
	 * this is a simple way to make sure the projects can be created
	 * without trying (and failing) to clobber each other
	 */
	private static final String cProjName = "MyFirstTestProject"; //$NON-NLS-1$
	private static final String cHelloWorldProjName = "MyFirstHelloWorldTestProject"; //$NON-NLS-1$
	private static final String cAutotoolsProjName = "MyFirstAutotoolsTestProject"; //$NON-NLS-1$
	private static final String cGTKProjName = "MyFirstGTKTestProject"; //$NON-NLS-1$
	private static final String cppProjName = "MyFirstCPPTestProject"; //$NON-NLS-1$
	private static final String testAuthor = "Ima Tester"; //$NON-NLS-1$

	
	@BeforeClass
	public static void beforeClass() throws Exception {
		bot = new SWTWorkbenchBot();
		bot.viewByTitle("Welcome").close();
		bot.perspectiveByLabel("C/C++").activate();
	}
	
	/* TODO: need to set the Yocto Project preferences first */
	
	/* java.lang.RuntimeException: java.lang.InterruptedException: New Project failure: Yocto Wizard Configuration Error:
	 * Specified Toolchain Root Location is empty.
	 * You need specify Toolchain Root Location before building any project.
	 * Do IDE-wide settings from Window > Preferences > Yocto Project SDK
	 * Or do Project-wide settings from Project > Change Yocto Project Settings.
	 */
	
	/* Test standard C Project creation, to make sure CDT is installed and working */
	@Test
	public void canCreateANewEmptyCProject() throws Exception {
		bot.menu("File").menu("New").menu("Project...").click();
		
		SWTBotShell shell = bot.shell("New Project");
		shell.activate();
		bot.tree().expandNode("C/C++").select("C Project");
		bot.button("Next >").click();
		
		bot.textWithLabel("Project name:").setText(cProjName);
		
		bot.button("Finish").click();
		
		assertProjectCreated(cProjName);
		assertTrue("New Project dialog should not be active after project creation.", !shell.isActive());
	}
	
	@Test
	public void canCreateANewANSICHelloWorldProject() throws Exception {
		bot.menu("File").menu("New").menu("Project...").click();
		
		SWTBotShell shell = bot.shell("New Project");
		shell.activate();
		bot.tree().expandNode("C/C++").select("C Project");
		bot.button("Next >").click();
		
		bot.textWithLabel("Project name:").setText(cHelloWorldProjName);
		bot.treeWithLabel("Project type:").expandNode("Executable").select("Hello World ANSI C Project");
		bot.button("Finish").click();
		assertProjectCreatedIsNotEmpty(cHelloWorldProjName);
		assertTrue("New Project dialog should not be active after project creation.", !shell.isActive());
	}
	
	/* Yocto Project SDK specific tests */
	/* FIXME: D.R.Y. these next three methods should be abstracted/simplified */
	@Test
	public void canCreateANewCAutotoolsProject() throws Exception {
		bot.menu("File").menu("New").menu("Project...").click();
		
		SWTBotShell shell = bot.shell("New Project");
		shell.activate();
		bot.tree().expandNode("C/C++").select("C Project");
		bot.button("Next >").click();
		
		bot.tree().expandNode("Yocto Project SDK Autotools Project").select("Hello World ANSI C Autotools Project");
		bot.textWithLabel("Project name:").setText(cAutotoolsProjName);
		bot.button("Next >").click();
		
		bot.textWithLabel("Author").setText(testAuthor);
		bot.button("Next >").click();

		bot.button("Finish").click();
		
		assertProjectCreatedIsNotEmpty(cAutotoolsProjName);
		
		try {
			assertTrue("New Project dialog should not be active after project creation.", !shell.isActive());
		} finally {
			// Allow testing to continue
			shell.close();
		}
		// TODO: should do something more interesting here, like build the project.
	}
	
	@Test
	public void canCreateANewGTKAutotoolsProject() throws Exception {
		bot.menu("File").menu("New").menu("Project...").click();
		
		SWTBotShell shell = bot.shell("New Project");
		shell.activate();
		bot.tree().expandNode("C/C++").select("C Project");
		bot.button("Next >").click();
		
		bot.tree().expandNode("Yocto Project SDK Autotools Project").select("Hello World GTK C Autotools Project");
		bot.textWithLabel("Project name:").setText(cGTKProjName);
		bot.button("Next >").click();
				
		bot.textWithLabel("Author").setText(testAuthor);
		bot.button("Next >").click();

		bot.button("Finish").click();
		
		assertProjectCreatedIsNotEmpty(cGTKProjName);
		
		try {
			assertTrue("New Project dialog should not be active after project creation.", !shell.isActive());
		} finally {
			// Allow testing to continue
			shell.close();
		}
	}

	@Test
	public void canCreateANewCPPAutotoolsProject() throws Exception {
		bot.menu("File").menu("New").menu("Project...").click();
		
		SWTBotShell shell = bot.shell("New Project");
		shell.activate();
		bot.tree().expandNode("C/C++").select("C++ Project");
		bot.button("Next >").click();
		
		bot.tree().expandNode("Yocto Project SDK Autotools Project").select("Hello World C++ Autotools Project");
		bot.textWithLabel("Project name:").setText(cppProjName);
		bot.button("Next >").click();

		bot.textWithLabel("Author").setText(testAuthor);
		bot.button("Next >").click();

		bot.button("Finish").click();

		assertProjectCreatedIsNotEmpty(cppProjName);
				
		// FIXME: Need to fix template so that New Project "shell" (aka dialog) closes on its own
		try {
			assertTrue("New Project dialog should not be active after project creation.", !shell.isActive());
		} finally {
			// Allow testing to continue
			shell.close();
		}
	}

	/* TODO need to add CMake projects */
	
	/* Helper methods */
	private void assertProjectCreated(String projName) {
		assertProjectCreated(projName, false);
	}
	
	private void assertProjectCreated(String projName, boolean shouldBeNonEmpty) {
		SWTBotView projectExplorerView = bot.viewByTitle("Project Explorer");
		projectExplorerView.show();
		Composite projectExplorerComposite = (Composite) projectExplorerView.getWidget();
		
		Tree swtTree = (Tree) bot.widget(WidgetMatcherFactory.widgetOfType(Tree.class), projectExplorerComposite);
		SWTBotTree tree = new SWTBotTree(swtTree);
		// throws WidgetNotFoundException (WNFE) if the item does not exist
		SWTBotTreeItem treeItem = tree.getTreeItem(projName).expand();
		if (shouldBeNonEmpty) {
			assertTrue(projName + " expected to be non-empty", !treeItem.getNodes().isEmpty());
		}
	}
	
	private void assertProjectCreatedIsNotEmpty(String projName) {
		assertProjectCreated(projName, true);
		
	}
	
	@AfterClass
	public static void sleep() {
		bot.sleep(2000);
	}

}
