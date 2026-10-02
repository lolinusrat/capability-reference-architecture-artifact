package com.enterprise.ai.runtime.cache.response;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/**
 * Regression test for the T3 finding: the cache key must be identical in every
 * process, or a shared (Redis) cache never hits across instances.
 *
 * <p>Two identically started JVMs can assign the same identity hash codes, so a
 * test between them would pass even with the defect. This test therefore runs
 * one plain JVM and one whose execution history has been perturbed (see
 * {@link CrossProcessKeyComputer}), and first confirms that the perturbation
 * really changed an identity-based hash: the pre-repair component,
 * {@code history().hashCode()}, must differ between the two processes. If it
 * does not, the test is reported as inconclusive (skipped) rather than passed.
 */
class ResponseCacheKeyCrossProcessTest {

    @TempDir
    Path dir;

    @Test
    @DisplayName("keys are identical across JVMs with different execution histories")
    void keysAreIdenticalAcrossDifferentlyPerturbedProcesses() throws Exception {
        List<String[]> plain = run("plain");
        List<String[]> perturbed = run("perturb");
        assertThat(perturbed).hasSameSizeAs(plain);

        boolean perturbationChangedLegacyHash = false;
        for (int i = 0; i < plain.size(); i++) {
            if (!plain.get(i)[2].equals(perturbed.get(i)[2])) {
                perturbationChangedLegacyHash = true;
            }
        }
        assumeTrue(perturbationChangedLegacyHash,
                "perturbation did not change identity-based hashes; the cross-process check is inconclusive");

        for (int i = 0; i < plain.size(); i++) {
            assertThat(perturbed.get(i)[1]).as("key for history case %s", i).isEqualTo(plain.get(i)[1]);
        }
    }

    @Test
    @DisplayName("role and order remain significant in the history digest")
    void roleAndOrderRemainSignificant() {
        ResponseCacheKeyFactory factory = new ResponseCacheKeyFactory();
        List<String> keys = CrossProcessKeyComputer.HISTORIES.stream()
                .map(history -> factory.key(CrossProcessKeyComputer.contextFor(history)))
                .toList();
        // 2 and 3 differ only by role; 4 and 5 only by order.
        assertThat(keys.get(2)).isNotEqualTo(keys.get(3));
        assertThat(keys.get(4)).isNotEqualTo(keys.get(5));
        assertThat(keys).doesNotHaveDuplicates();
    }

    private List<String[]> run(String mode) throws Exception {
        Path out = dir.resolve(mode + ".tsv");
        Path java = Path.of(System.getProperty("java.home"), "bin", "java");
        Process process = new ProcessBuilder(java.toString(), "-cp", System.getProperty("java.class.path"),
                CrossProcessKeyComputer.class.getName(), mode, out.toString())
                .redirectErrorStream(true)
                .start();
        assertThat(process.waitFor(120, TimeUnit.SECONDS)).as("child JVM finished").isTrue();
        assertThat(process.exitValue()).as("child JVM exit status: %s",
                new String(process.getInputStream().readAllBytes())).isZero();
        return Files.readAllLines(out).stream().map(line -> line.split("\t")).toList();
    }
}
