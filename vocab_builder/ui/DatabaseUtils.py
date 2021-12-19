from vocab_builder.infrastructure import get_session
from vocab_builder.ui.AnkiUtils import get_addon_dir

prod_session = get_session(get_addon_dir())
