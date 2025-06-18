<script lang="ts">
	import '../app.css';
	import { ModeWatcher } from "mode-watcher";
	let { children } = $props();
</script>
<svelte:head>
	<title>Luis Fialho</title>
</svelte:head>
<ModeWatcher track={false} defaultMode={"dark"}/>


{@render children()}

