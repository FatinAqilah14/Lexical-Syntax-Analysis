// Generated from rules.g by ANTLR 4.7.2
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link rulesParser}.
 */
public interface rulesListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link rulesParser#prog}.
	 * @param ctx the parse tree
	 */
	void enterProg(rulesParser.ProgContext ctx);
	/**
	 * Exit a parse tree produced by {@link rulesParser#prog}.
	 * @param ctx the parse tree
	 */
	void exitProg(rulesParser.ProgContext ctx);
	/**
	 * Enter a parse tree produced by {@link rulesParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterExpr(rulesParser.ExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link rulesParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitExpr(rulesParser.ExprContext ctx);
}