// don't import css, cause it duplicates? shares the same bundle with index
import Api from './pages/Api.svelte';

const app = new Api({
	target: document.body
});

export default app;
