<?php

// Set the time limit to unlimited to handle long calculations
set_time_limit(0);

$iterations = 1000000000;  // Number of iterations
$result = 1;

for ($i = 1; $i <= $iterations; $i++) {
    $result *= 1.000001;  // Small multiplication to avoid overflow
    if ($i % 100000 == 0) {
        echo "Iteration $i: Result = " . number_format($result, 10) . PHP_EOL;
    }
}

echo "Final Result: " . number_format($result, 10) . PHP_EOL;

?>

