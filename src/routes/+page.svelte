<script lang="ts">
	import '../app.css';
	import '@fontsource-variable/eb-garamond';
	import { Button } from "$lib/components/ui/button/index.js";
	import { toggleMode } from "mode-watcher";

	const sections = ["writing", "code", "curricula", "music", "video"]
	const sectNum = sections.length

</script>
<div class="bg-[url('/images/bg_01.jpg')] w-screen bg-cover bg-center min-h-screen p-2">

<div class="border sm:grid grid-flow-col grid-cols-4 space-y-3 p-3 gap-2">
	<div class="grid gap-6">
		<div class="sm:p-1 border">
			<a href="recent" class="border block">
			<div class="sm:p-4 mb-6 p-2 rounded-l transition duration-900 mask-r-from-0% mask-l-from-70% mask-t-from-80% mask-b-from-80% hover:bg-violet-300/60 ">
			<h1 class="border sm:text-3xl text-xl text-white font-serif p-2 italic overline">recent work</h1>
			</div>
			</a>
		</div>
		{#each sections as section}
			<a href="{section}" class="border block h-fit">
			<div class="sm:p-15 p-2 rounded-l transition duration-900 mask-r-from-0% mask-l-from-70% mask-t-from-80% mask-b-from-80% hover:bg-violet-200/30 ">
			<h1 class="border sm:text-3xl text-xl text-white font-serif ml-12 h-fit p-2">{section}</h1>
			</div>
			</a>
		{/each}
		<!--<div class="h-fit sm:p-15 p-5 border">
		</div>-->
	</div>
	<div class="lg:border mx-6">
	</div>
	<div class="border sm:grid col-span-2 p-4 gap-2">
		<div class="border col-span-4 p-1">
		<h1 class="border md:text-4xl text-2xl text-white font-serif lg:mx-12 mx-2 mt-12 col-span-4 p-2"><a href="about" class="transition duration-700 sm:p-5 hover:text-violet-100 opacity-70 hover:opacity-100">Luis M. Fialho</a></h1>
		</div>
		{#each {length: sectNum} as num}
		<div class="md:border col-span-4 p-1"></div>
		{/each}
		<div class="border col-span-4 p-2">
			<br>
			<p class="sm:text-lg text-md text-white font-serif ml-10 h-fit sm:mt-10">This website is a portfolio of the work I have done professionally, academically, and personally.</p>
			<p class="sm:text-lg text-md text-white font-serif ml-10 h-fit mt-5">contact: email</p>
		</div>
	</div>
</div>
<div class="">
	<div class="border mt-3">
		<Button onclick={toggleMode} variant="ghost" class="object-center text-white mask-r-from-70% mask-l-from-70% mask-t-from-60% mask-b-from-60% dark:hover:bg-input/70 hover:bg-input/20 hover:text-white">Frames</Button>
	</div>
</div>
</div>