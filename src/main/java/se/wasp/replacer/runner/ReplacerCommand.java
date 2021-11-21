package se.wasp.replacer.runner;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import picocli.CommandLine;
import spoon.Launcher;
import spoon.reflect.CtModel;
import spoon.reflect.code.CtLiteral;
import spoon.reflect.cu.SourcePosition;
import spoon.reflect.visitor.Filter;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.List;
import java.util.concurrent.Callable;

@CommandLine.Command(name = "replacer", mixinStandardHelpOptions = true, version = "1.0",
        description = "Replace strings in java programs")
public class ReplacerCommand implements Callable<Integer> {
    @CommandLine.Option(names = {"-n", "--new-str"}, description = "New string")
    private String newStr;

    @CommandLine.Option(names = {"-os", "--old-str"}, description = "The old string AST node identifier")
    private String oldStrId;

    @CommandLine.Option(names = {"-of", "--output-file"}, description = "Path to output diff file")
    private String outputPath;

    private Launcher launcher = new Launcher();
    private CtModel model;

    @Override
    public Integer call() throws Exception {
        String[] oldStrIdParts = oldStrId.split(",");
        File oldSrc = new File(oldStrIdParts[oldStrIdParts.length - 8]);
        final int oldLine = Integer.parseInt(oldStrIdParts[1]), oldCol = Integer.parseInt(oldStrIdParts[3]),
                oldEndLine = Integer.parseInt(oldStrIdParts[2]), oldEndCol = Integer.parseInt(oldStrIdParts[4]);

        File newDir = Files.createTempDirectory("src").toFile();

        launcher.getEnvironment().setCommentEnabled(true);
        launcher.addInputResource(oldSrc.getAbsolutePath());
        launcher.buildModel();
        model = launcher.getModel();

        CtLiteral literal = model.filterChildren(new Filter<CtLiteral>() {
            @Override
            public boolean matches(CtLiteral element) {
                SourcePosition pos = element.getPosition();
                return pos.isValidPosition() && pos.getLine() == oldLine && pos.getColumn() == oldCol &&
                        pos.getEndLine() == oldEndLine && pos.getEndColumn() == oldEndCol;
            }
        }).first();

        literal.setValue(newStr);

        launcher.setSourceOutputDirectory(newDir);
        launcher.prettyprint();
        File newSrc = newDir.listFiles()[0];

        ProcessBuilder pb =
                new ProcessBuilder("git", "diff", "--no-index", oldSrc.getAbsolutePath(),
                        newSrc.getAbsolutePath()).redirectOutput(new File(outputPath));
        Process p = pb.start();
        p.waitFor();

        removeLast(new File(outputPath));

        return 0;
    }

    private void removeLast(File file) throws IOException {
        List<String> lines = FileUtils.readLines(file, "UTF-8");
        lines = lines.subList(0, lines.size() - 1);
        FileUtils.writeLines(file, lines);
    }
}
