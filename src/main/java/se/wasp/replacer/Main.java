package se.wasp.replacer;

import picocli.CommandLine;
import se.wasp.replacer.runner.ReplacerCommand;

public class Main {
    public static void main(String[] args) {
        int exitCode = new CommandLine(new ReplacerCommand()).execute(args);
        System.exit(exitCode);
    }
}
