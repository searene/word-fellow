from vocab_builder.infrastructure import get_session, get_vocab_builder_db
from vocab_builder.ui.AnkiUtils import get_addon_dir

prod_session = get_session(get_addon_dir())
prod_vocab_builder_db = get_vocab_builder_db(get_addon_dir())
