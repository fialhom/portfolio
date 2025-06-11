<script lang="ts">
	import '../../app.css';
	import { ModeWatcher } from "mode-watcher";
	let { children } = $props();
</script>

<ModeWatcher track={false} defaultMode={"dark"}/>
{@render children()}

