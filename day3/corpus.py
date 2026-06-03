 
DOCS = [
    "Helios is a stream-processing command-line tool built by the (fictional) Aurora Data team in 2024. It moves and transforms event data between systems.",
    "The Helios daemon listens on port 7330 by default. You can change it with the `--port` flag or the `server.port` key in the config file.",
    "Helios reads its configuration from ~/.helios/config.yaml. If that file is missing, Helios falls back to built-in defaults and prints a warning.",
    "By default Helios runs 8 parallel workers. This is configurable up to a maximum of 64 workers via the `runtime.max_workers` setting.",
    "When a pipeline step fails, Helios retries it 3 times using exponential backoff, starting at 2 seconds and doubling each attempt.",
    "Helios supports three source connectors out of the box: Apache Kafka, Amazon S3, and PostgreSQL. Additional connectors can be added as plugins.",
    "The main commands are `helios run` to start a pipeline, `helios validate` to check a config without running it, and `helios status` to inspect running pipelines.",
    "The free tier of Helios allows up to 5 concurrent pipelines. Running more than 5 requires a paid license key set via the HELIOS_LICENSE environment variable.",
    "Helios stores its internal state in an embedded SQLite database at ~/.helios/state.db. Deleting this file resets all pipeline checkpoints.",
    "Helios emits Prometheus-compatible metrics at the /metrics endpoint on the same port as the daemon, so it can be scraped by standard monitoring stacks.",
]

CHUNKS = {i: text for i, text in enumerate(DOCS)}

SAMPLE_QUERIES = [
    "What port does Helios use by default?",
    "How many parallel workers does Helios run, and what's the maximum?",
    "How does Helios handle a step that fails?",
    "Which databases and message systems can Helios read from?",
    "Who won the 2022 FIFA World Cup?",  # off-topic -> should be 'I don't know'
]
 