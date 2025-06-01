<script lang="ts">
	import '../app.css';
	import '@fontsource-variable/eb-garamond';
	import { Button } from "$lib/components/ui/button/index.js";
	import { toggleMode } from "mode-watcher";

	const sections = ["Writing", "Curricula", "Code", "Music", "Video"]
	const sectNum = sections.length
	console.log(sectNum)
</script>

<div class="bg-[url('/images/bg.jpg')] w-screen bg-cover bg-center min-h-screen p-2">
	<div class="p-1"></div>
	<!--<div class="p-3 flex items-center">
			<Button href="about" variant="ghost" class="object-center text-white bg-input/10 border-input hover:bg-input/20 hover:text-white">About</Button>
	</div>-->

	<div class="border sm:grid grid-flow-col grid-cols-4 space-y-3 p-3 gap-2">
		<div class="grid gap-6">
			{#each sections as section}
				<a href="{section}" class="border block h-fit">
				<div class="sm:p-15 p-2 rounded-l transition duration-900 mask-r-from-0% mask-l-from-70% mask-t-from-80% mask-b-from-80% hover:bg-violet-200/20 ">
				<h1 class="border sm:text-3xl text-xl text-white font-serif ml-10 h-fit p-2">{section}</h1>
				</div>
				</a>
			{/each}
			<div class="h-fit sm:p-15 p-5 border"></div>
		</div>
		<div class="sm:border mx-6"></div>
		<div class="border sm:grid col-span-2 p-4 gap-2">
			<h1 class="sm:text-3xl text-xl text-white font-serif ml-10 mt-10">Luis M. Fialho</h1>
			{#each {length: sectNum} as num}
			<div class="border col-span-4 p-1"></div>
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
			<Button onclick={toggleMode} variant="ghost" class="object-center text-white mask-r-from-70% mask-l-from-70% mask-t-from-60% mask-b-from-60% dark:hover:bg-input/20 hover:bg-input/20 hover:text-white">Frames</Button>
		</div>
	</div>
</div>