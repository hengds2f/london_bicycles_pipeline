import great_expectations as gx
context = gx.get_context(mode="ephemeral")
context.add_expectation_suite(expectation_suite_name="trips_suite")
context.add_expectation_suite(expectation_suite_name="stations_suite")
print("Successfully created suites")
