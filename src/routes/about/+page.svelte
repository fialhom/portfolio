<script lang="ts">
    import '../../app.css';
	import '@fontsource-variable/eb-garamond';

	import { Button } from "$lib/components/ui/button/index.js";
	import { toggleMode } from "mode-watcher";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";

    import { page } from '$app/state';
   // import data  from '$lib/data/portfolio_data.json';

    const slugurl = page.params.slug
</script>

<div class="bg-[url('/images/bg_022.jpg')] w-screen bg-cover bg-center min-h-screen p-2">
		<div class="grid gap-6">
		<div class="sm:p-1 border">
			<a href="/" class="border block">
			<div class="sm:p-4 mb-6 p-2 rounded-l transition duration-900 mask-r-from-0% mask-l-from-90% mask-t-from-80% mask-b-from-80% hover:bg-violet-300/60 ">
			<h2 class="border sm:text-2xl text-lg text-white font-serif p-2 italic overline">homepage</h2>
			</div>
			</a>
		</div>
		</div>
	<div class="">
		<p>Description</p>
	</div>
	<div class="">
		<div class="border mt-3">
			<Button onclick={toggleMode} variant="ghost" class="object-center text-white mask-r-from-70% mask-l-from-70% mask-t-from-60% mask-b-from-60% dark:hover:bg-input/70 hover:bg-input/20 hover:text-white">Frames</Button>
		</div>
	</div>
</div>