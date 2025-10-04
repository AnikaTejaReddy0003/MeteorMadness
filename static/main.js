import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Get the container element from the HTML
const container = document.getElementById('canvas-container');

// 1. Scene, Camera, and Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ 
    antialias: true,
    alpha: true // This is the key for a transparent background!
});

renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

// We don't set a scene background color, so the renderer's alpha can show through.

// 2. Add Lights
const ambientLight = new THREE.AmbientLight(0xffffff, 0.8); // Slightly brighter ambient light
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
scene.add(directionalLight);

// 3. Load the GLTF Model
const loader = new GLTFLoader();
loader.load(
    'model/scene.gltf', // <-- Make sure this path is correct!
    function (gltf) {
        const model = gltf.scene;
        model.scale.set(1.5, 1.5, 1.5); // Adjust scale to fit the container
        scene.add(model);
        animate(model); // Start animation loop after loading
    },
    undefined, 
    function (error) {
        console.error('An error happened while loading the model:', error);
    }
);

// 4. Set Camera Position and Controls
camera.position.z = 150; // Adjusted camera distance
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enablePan = false; // Optional: disable panning
controls.enableZoom = false; // Optional: disable zooming

// 5. Animation Loop
function animate(model) {
    requestAnimationFrame(() => animate(model));

    // Add continuous rotation
    if (model) {
        model.rotation.y += 0.002;
    }

    controls.update();
    renderer.render(scene, camera);
}

// Handle window resizing
window.addEventListener('resize', () => {
    // Update camera aspect ratio and renderer size based on the container
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
});