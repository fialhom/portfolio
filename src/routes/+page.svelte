<script lang="ts">
	import '../app.css';
	import { Button } from "$lib/components/ui/button/index.js";

	const sections = ["Writing", "Music", "Video", "Code", "Curricula"]
</script>

<div class="bg-[url('/images/bg.jpg')] w-screen bg-cover bg-center min-h-screen">

	<div class="p-3 flex justify-end items-center">
		<div class="">
			<Button href="about" variant="ghost" class="object-center text-white bg-input/10 border-input hover:bg-input/20 hover:text-white">About</Button>
		</div>
	</div>

	<div class="space-y-3 p-3 ">
		<div class="grid gap-6">
			{#each sections as section}
				<a href="{section}" class="block h-fit">
				<div class="p-15 rounded transition duration-1000 mask-r-from-10% hover:bg-violet-200/30">
				<h1 class="text-xl text-white ml-10">{section}</h1>
				</div>
				</a>
			{/each}
		</div>
	</div>
</div>