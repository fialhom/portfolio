<script lang="ts">
    import '../../app.css';
	import '@fontsource-variable/eb-garamond';

    import { Input } from "$lib/components/ui/input/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { toggleMode } from "mode-watcher";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";

    import { page } from '$app/state';
    import data  from '$lib/data/metadata.json';

    const slugurl = page.params.slug;
    let search: string = $state<string>('');

</script>

<div class="bg-[url('/images/bg_022.jpg')] w-screen bg-cover bg-center min-h-screen p-2">
<div class="border sm:grid grid-flow-col grid-cols-1 space-y-3 p-3 gap-2">
	<div class="gap-6 space-y-1">
		<div class="sm:p-1 border space-y-2">
			<a href="/" class="border block">
			<div class="sm:p-4 p-2 rounded-l transition duration-900 mask-r-from-0% mask-l-from-90% mask-t-from-80% mask-b-from-80% hover:bg-violet-300/60 ">
			<h2 class="border sm:text-2xl text-lg text-white font-serif p-2 italic overline">homepage</h2>
			</div>
			</a>
            <div class="p-1">
            <Input placeholder="filter" class="dark:border-input ml-15 w-1/2 dark:bg-transparent bg-transparent text-white placeholder:text-white/30 dark:focus:border-white/60 focus:border-white/60 mask-r-from-30%" bind:value={search}/>
            </div>
		</div>
        
        <ScrollArea class="sm:max-h-[80vh] max-h-[70vh] overflow-auto" type="auto">
        <div class="border grid grid-cols-8 p-2 space-y-5 space-x-2">
            
            {#each data as entry}
            {#if entry.category === slugurl}
                <div class="border p-1 col-span-2"></div>
                <div class="border p-1 col-span-5 space-y-1">
                    <div class="border p-2">
                        <a href="{entry.url}" class="h-fit">
                        <div class="p-2 rounded-l transition duration-900 sm:mask-r-from-80% mask-l-from-90% mask-t-from-80% mask-b-from-80% hover:bg-violet-200/30 ">
                            <h2 class="dark:underline decoration-dotted sm:underline-offset-10 border sm:text-3xl text-xl text-white font-serif h-fit sm:ml-15">{entry.title}</h2>
                            <p class="border text-white mt-1 sm:ml-15 font-serif font-light sm:text-lg text-md italic">{entry.date.slice(0,4)}</p>
                            <p class="border text-white mt-1 sm:ml-15 sm:mr-15 font-serif sm:text-lg text-md">{entry.description}</p>
                        </div>
                        </a>
                    </div>
                </div>
                <div class="border p-1 col-span-1"></div>
            {/if}
            {/each}
        </div>
    </ScrollArea>
	</div>
</div>
<div class="">
	<div class="border mt-3">
		<Button onclick={toggleMode} variant="ghost" class="object-center text-white mask-r-from-70% mask-l-from-70% mask-t-from-60% mask-b-from-60% dark:hover:bg-input/70 hover:bg-input/20 hover:text-white">Frames</Button>
	</div>
</div>
</div>