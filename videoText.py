import random

# A comprehensive list of video title and description pairs with hashtags
video_texts = [
    {"title": "Peaceful Ocean Breeze 🌊 #Calming #SleepMusic #Mindfulness #Tranquil", 
     "description": "Relax and breathe deeply as the calming ocean breeze sweeps through your mind. Perfect for meditation or simply unwinding after a long day. Let the soothing sounds of the sea wash over you, bringing peace and serenity. Ideal for deep sleep and stress relief. #OceanSounds #Meditation #StressRelief #PeacefulSleep #CalmingVibes #Mindfulness #Zen #Relaxation"},
    
    {"title": "Gentle Forest Sounds 🌳 #Calming #NatureLovers #Zen #AmbientMusic", 
     "description": "Immerse yourself in the gentle whispers of the forest. Birds chirp peacefully, and leaves rustle in the wind. The natural symphony will bring a sense of calm and grounding to your body and mind. This serene environment is perfect for meditation and relaxation. #ForestSounds #NatureSounds #Meditation #Relaxation #StressRelief #Mindfulness #Zen #CalmingVibes"},
    
    {"title": "Healing Sounds of Nature 🌿 #AmbientMusic #Zen #Mindfulness #Calm", 
     "description": "Healing sounds from nature designed to rejuvenate your body and mind. Let the serene sounds of flowing water and birdsong guide you into a deep state of relaxation. Ideal for stress relief, meditation, and a peaceful sleep. A natural escape from the chaos of daily life. #NatureSounds #HealingMusic #Meditation #StressRelief #Mindfulness #CalmingVibes #Zen #Relaxation"},
    
    {"title": "Tranquil Rainstorm Sounds 🌧️ #CalmingVibes #PeacefulSleep", 
     "description": "Feel the calming presence of a gentle rainstorm. The steady rhythm of raindrops creates a peaceful atmosphere, perfect for relaxation. Ideal for soothing your mind after a busy day or for creating a calming background while you work or study. A peaceful retreat for your soul. #RainSounds #SleepMusic #StressRelief #Relaxation #Meditation #Mindfulness #CalmingVibes #PeacefulSleep"},
    
    {"title": "Calming Wind Chimes 🎐 #WindChimes #Zen", 
     "description": "The delicate sound of wind chimes carried by the breeze will help you find peace. The soft tones create a serene atmosphere, perfect for mindfulness and meditation. Allow yourself to drift away with the gentle sound of chimes and feel your stress melt away. #WindChimes #Meditation #Mindfulness #Zen #CalmingVibes #StressRelief #Relaxation #PeacefulSleep"},
    
    {"title": "Mystic Night Sounds 🌙 #NightSounds #PeacefulSleep #Zen", 
     "description": "The stillness of the night, enhanced by gentle ambient sounds, brings a feeling of mystery and calm. This soothing atmosphere is perfect for deep meditation or peaceful sleep. Let go of the day's stress and relax into a serene dream. The perfect companion for late-night relaxation. #NightSounds #Meditation #PeacefulSleep #Zen #StressRelief #Mindfulness #CalmingVibes #Relaxation"},
    
    {"title": "Deep Sleep Music 😴 #DeepSleepMusic #PeacefulSleep #RestfulNight", 
     "description": "Gentle music designed to guide you into deep, restful sleep. Let the peaceful melodies ease your mind and help you let go of stress. Ideal for a relaxing environment at bedtime or to use while meditating. Perfect for those seeking quality sleep and relaxation. #SleepMusic #DeepSleep #Meditation #StressRelief #Relaxation #Mindfulness #PeacefulSleep #CalmingVibes"},
    
    {"title": "Zen Garden Ambience 🏞️ #CalmingVibes #PeacefulMusic #Tranquility", 
     "description": "Relax in the tranquility of a Zen garden, surrounded by the calming sounds of nature. The rhythmic sound of water flowing and leaves rustling provides a peaceful backdrop for meditation or mindfulness practice. This calming environment promotes relaxation and helps clear your mind. #ZenGarden #Meditation #Mindfulness #CalmingVibes #StressRelief #Relaxation #PeacefulMusic #Tranquility"},
    
    {"title": "Meditative Ocean Waves 🌊 #PeacefulSleep #Tranquil", 
     "description": "Let the soothing sound of ocean waves calm your mind and soul. The ebb and flow of the tide help promote relaxation and mindfulness. Perfect for deep meditation, relaxation, or as a sleep aid. Allow the ocean to take you on a journey of calm and tranquility. #OceanWaves #Meditation #PeacefulSleep #Tranquil #StressRelief #Mindfulness #Relaxation #CalmingVibes"},
    
    {"title": "Pure Relaxation with Rain Sounds 🌧️ #PeacefulSleep #Zen", 
     "description": "Rain sounds are known to promote relaxation and focus. Let the rhythmic patter of raindrops relax your body and mind. Ideal for meditation, deep sleep, or unwinding after a busy day. The calming sound of rain will help you let go of stress and create a peaceful environment. #RainSounds #PeacefulSleep #Zen #Meditation #StressRelief #Relaxation #Mindfulness #CalmingVibes"},
    
    {"title": "Binaural Beats for Meditation 🎧 #PeacefulMind #MentalClarity", 
     "description": "Experience deep meditation with binaural beats designed to calm the mind and enhance your focus. These peaceful frequencies promote relaxation and mental clarity. Perfect for mindfulness practice, relaxation, and stress relief. Allow your mind to be at ease with these calming beats. #BinauralBeats #Meditation #MentalClarity #StressRelief #Mindfulness #Focus #CalmingVibes #PeacefulMind"},
    
    {"title": "Serenity by the Waterfall 🌊 #StressRelief #Mindfulness", 
     "description": "Feel the calming energy of a peaceful waterfall. The sound of cascading water brings a sense of calm and serenity to your environment. Ideal for meditation, relaxation, or simply unwinding after a busy day. Let the natural sounds of the waterfall rejuvenate your spirit. #WaterfallSounds #StressRelief #Mindfulness #Meditation #Relaxation #CalmingVibes #NatureSounds #PeacefulSleep"},
    
    {"title": "Gentle Creek Sounds 🌊 #PeacefulSleep", 
     "description": "The soft murmur of a creek running through the forest provides the perfect ambiance for relaxation and meditation. The gentle sound of flowing water is ideal for enhancing mindfulness or promoting a restful night's sleep. Allow the creek's calming flow to ease your mind and soul. #CreekSounds #PeacefulSleep #Meditation #Mindfulness #Relaxation #NatureSounds #StressRelief #CalmingVibes"},
    
    {"title": "Meditation Music for Stress Relief 🧘‍♀️ #PeacefulMind", 
     "description": "Listen to this calming music designed specifically for stress relief. With gentle tones and peaceful melodies, this music helps clear your mind and promotes deep relaxation. Perfect for meditation, yoga, or creating a peaceful atmosphere at home. #MeditationMusic #StressRelief #PeacefulMind #Relaxation #Yoga #Mindfulness #CalmingVibes #PeacefulSleep"},
    
    {"title": "Sleep Sounds of the Jungle 🌴 #PeacefulSleep #Zen #AmbientMusic", 
     "description": "The sounds of the jungle, with its gentle night creatures and whispering leaves, bring a peaceful ambiance to any environment. Perfect for those who enjoy a natural soundscape while drifting off to sleep. Let the soothing sounds of the jungle carry you into a restful, peaceful slumber. #JungleSounds #PeacefulSleep #Zen #AmbientMusic #NatureSounds #Meditation #StressRelief #Relaxation"},
    
    {"title": "Whispers of the Ocean Tide 🌊 #OceanTide #ZenMusic",
     "description": "Allow the whispers of the ocean tide to soothe your soul. The rhythmic sound of the waves gently rolling ashore promotes deep relaxation and mindfulness. Perfect for meditation or as a peaceful sleep aid, let the ocean's energy bring tranquility to your mind and body. #OceanTide #ZenMusic #Meditation #Mindfulness #Relaxation #StressRelief #PeacefulSleep #CalmingVibes"},
    
    {"title": "Soothing Desert Winds 🌵 #CalmingVibes #Mindfulness #ZenMusic",
     "description": "Feel the gentle embrace of desert winds sweeping across the sand. The quiet stillness and rhythmic gusts create a peaceful atmosphere that invites calm and relaxation. Ideal for mindfulness, meditation, or just unwinding after a busy day. #DesertWinds #CalmingVibes #Mindfulness #ZenMusic #Meditation #StressRelief #Relaxation #PeacefulSleep"},
    
    {"title": "Mystical Forest Ambience 🌲 #ForestAmbience #ZenVibes",
     "description": "Step into a magical forest where nature whispers softly. Birds sing, leaves rustle, and distant creatures create a serene soundtrack for your mind. Perfect for meditation, relaxation, or simply unwinding into the peaceful embrace of the forest. #ForestAmbience #ZenVibes #Meditation #Relaxation #NatureSounds #Mindfulness #StressRelief #PeacefulSleep"},
    
    {"title": "Silent Snowfall 🌨️ #SnowfallSounds #WinterRelaxation #Mindfulness",
     "description": "The quiet elegance of a snowfall provides a calm, serene backdrop for relaxation and meditation. The soft crunch of snow underfoot and the hushed atmosphere invite a sense of stillness. Let the snowy ambiance soothe your mind and promote peaceful sleep. #SnowfallSounds #WinterRelaxation #Mindfulness #Meditation #StressRelief #PeacefulSleep #CalmingVibes #Relaxation"},
    
    {"title": "Serenity in the Meadow 🌼 #MeadowSounds #PeacefulSleep",
     "description": "Breathe deeply as you relax in the tranquil meadow, where the gentle hum of nature surrounds you. The sound of bees buzzing, birds chirping, and a soft breeze blowing through the flowers creates a serene environment ideal for stress relief, meditation, and sleep. #MeadowSounds #PeacefulSleep #Meditation #StressRelief #NatureSounds #Mindfulness #Relaxation #CalmingVibes"},
    
    {"title": "Tranquil River Flow 🌊 #RiverSounds #NatureVibes",
     "description": "Let the calming flow of the river guide you into a peaceful state. The soothing sound of water gently cascading over rocks promotes deep relaxation and a sense of connection with nature. Ideal for unwinding, meditation, or simply escaping the stresses of the day. #RiverSounds #NatureVibes #Meditation #Relaxation #StressRelief #Mindfulness #PeacefulSleep #CalmingVibes"},
    
    {"title": "Gentle Mountain Breeze 🏔️ #MountainBreeze #ZenMusic",
     "description": "The cool mountain breeze whispers through the pines, offering a refreshing sense of calm. This peaceful environment helps clear your mind and brings relaxation to your body. Perfect for meditation, mindful moments, or a restful night's sleep. #MountainBreeze #ZenMusic #Meditation #Mindfulness #Relaxation #StressRelief #PeacefulSleep #CalmingVibes"},
    
    {"title": "Lullaby of the Ocean 🌊 #OceanLullaby #StressRelief #ZenVibes",
     "description": "Drift away to the lullaby of the ocean as waves gently crash against the shore. This soothing melody provides the perfect soundtrack for sleep, meditation, or stress relief. Let the ocean's rhythm bring peace to your mind and help you unwind. #OceanLullaby #StressRelief #ZenVibes #PeacefulSleep #Meditation #Relaxation #Mindfulness #CalmingVibes"},
    
    {"title": "Whispers of the Wind 🌬️ #WindSounds #ZenMusic",
     "description": "The soft whispers of the wind through the trees offer a peaceful escape from the chaos of daily life. Ideal for relaxation, meditation, and mindfulness, this serene breeze will help ease your mind and promote a sense of tranquility. #WindSounds #ZenMusic #Meditation #Relaxation #Mindfulness #StressRelief #PeacefulSleep #CalmingVibes"},
    
    {"title": "Raindrops on Leaves 🌧️🍃 #StressRelief #PeacefulMusic",
     "description": "Listen as raindrops gently tap on the leaves, creating a soothing rhythm that brings peace to your mind. Perfect for meditation, relaxation, or as a calming sleep aid, the soft rain will help you let go of stress and create a peaceful environment. #Raindrops #StressRelief #PeacefulMusic #Meditation #Relaxation #Mindfulness #PeacefulSleep #CalmingVibes"},
    
    {"title": "Morning Dew in the Forest 🌿 #PeacefulSleep #CalmingMusic",
     "description": "Experience the fresh and invigorating sounds of the forest at dawn. The dew on the leaves, the birds beginning to sing, and the soft morning breeze bring a sense of peace. Perfect for starting your day with mindfulness or unwinding after a busy one. #MorningDew #PeacefulSleep #CalmingMusic #Mindfulness #Meditation #NatureSounds #StressRelief #Relaxation"},
    
    {"title": "Calming Underwater Sounds 🌊🐠 #Mindfulness #ZenMusic",
     "description": "Immerse yourself in the calming sounds of the underwater world. Hear the soft hum of distant waves and the rhythmic ebb of the tides as they gently flow over coral reefs. Ideal for relaxation, deep sleep, or meditation, let the tranquil sounds of the sea soothe you. #UnderwaterSounds #Mindfulness #ZenMusic #Relaxation #PeacefulSleep #Meditation #StressRelief #CalmingVibes"},
    
    {"title": "Tropical Rainforest Harmony 🍃🌴 #Relaxation #StressRelief #PeacefulSleep",
     "description": "Immerse yourself in the lush, vibrant sounds of the tropical rainforest. The chorus of birds, rustling leaves, and gentle rain create a harmonious, peaceful environment perfect for relaxation, meditation, and sleep. #RainforestHarmony #Relaxation #StressRelief #PeacefulSleep #Meditation #NatureSounds #Mindfulness #CalmingVibes"},
    
    {"title": "Quiet Morning at the Lake 🌅 #Relaxation #Meditation #Zen",
     "description": "The quiet beauty of a morning at the lake sets the perfect tone for a day of calm. The stillness of the water, birds in the distance, and the soft rustle of the breeze invite you to relax and reflect. Ideal for meditation, relaxation, and peaceful sleep. #LakeMorning #Relaxation #Meditation #Zen #Mindfulness #PeacefulSleep #StressRelief #CalmingVibes"},
    
    {"title": "Echoes of the Canyon 🏞️ #Mindfulness #Zen",
     "description": "The echoing sounds of nature in a canyon bring a sense of vastness and serenity. The distant calls of birds, the rustling of rocks, and the soft winds create an atmosphere of quiet reflection. Perfect for unwinding, deep meditation, or simply connecting with nature. #CanyonEchoes #Mindfulness #Zen #Meditation #Relaxation #NatureSounds #StressRelief #PeacefulSleep"},
    
    {"title": "Glistening Waterfall Sounds 🌊 #PeacefulSleep #ZenVibes",
     "description": "Feel the refreshing energy of a glistening waterfall as the water cascades down the rocks. This calming sound promotes relaxation, mindfulness, and peaceful sleep. Let the rhythm of the falls wash away your worries and clear your mind. #WaterfallSounds #PeacefulSleep #ZenVibes #Meditation #Mindfulness #StressRelief #Relaxation #CalmingVibes"},
    
    {"title": "Breeze Through Bamboo 🌾 #PeacefulSleep #Zen",
     "description": "Relax in the calming ambiance of a bamboo forest, where the breeze whispers through the tall stalks. The soft rustling of bamboo creates an atmosphere of peace and relaxation. Perfect for mindfulness, meditation, or drifting off into a peaceful sleep. #BambooBreeze #PeacefulSleep #Zen #Mindfulness #Meditation #StressRelief #Relaxation #CalmingVibes"},
    
    {"title": "Sunset by the Ocean 🌅 #Mindfulness #PeacefulMusic",
     "description": "Experience the tranquility of a sunset by the ocean. The gentle waves and soft winds create a peaceful, serene environment that's perfect for unwinding after a long day. Ideal for meditation, relaxation, and peaceful sleep. #OceanSunset #Mindfulness #PeacefulMusic #Meditation #Relaxation #StressRelief #PeacefulSleep #CalmingVibes"},
    
    {"title": "Pine Forest Tranquility 🌲 #Mindfulness #ZenVibes",
     "description": "Let the calming sounds of the pine forest wash over you. The soft rustling of pine needles and the crisp air invite peace and relaxation. Perfect for meditation, mindfulness practice, or simply unwinding in nature's embrace. #PineForest #Mindfulness #ZenVibes #Meditation #Relaxation #NatureSounds #StressRelief #PeacefulSleep"},
    
    {"title": "Deep Forest Rainfall 🌧️🌲 #Mindfulness",
     "description": "The sound of gentle rain falling in a deep forest creates a cozy, calming atmosphere. Perfect for deep relaxation, meditation, or sleep, this peaceful soundscape will help you unwind and reconnect with nature. #ForestRainfall #Mindfulness #Meditation #Relaxation #NatureSounds #StressRelief #PeacefulSleep #CalmingVibes"},
    
    {"title": "Calming Waves of Serenity 🌊", 
     "description": "The gentle ebb and flow of ocean waves will transport you to a serene space, ideal for meditation, relaxation, and peaceful sleep. Let the natural rhythm soothe your body and mind, promoting stress relief and deep rest. #SleepMusic #Relaxation #Meditation #OceanSounds #Mindfulness #PeacefulSleep #StressRelief #CalmingVibes"},
    
    {"title": "Gentle Night Rain Sounds 🌧️", 
     "description": "Relax and unwind to the soothing sound of a gentle night rainstorm. This calming backdrop helps reduce stress, improve sleep quality, and enhance meditation practices. #RainSounds #SleepMusic #StressRelief #Relaxation #Meditation #Mindfulness #PeacefulSleep #CalmingVibes"},
    
    {"title": "Soothing Piano for Restful Sleep 🎹", 
     "description": "Let the soft, melodic piano notes guide you into a deep, restful sleep. Perfect for relaxation, meditation, or simply creating a calming environment before bedtime. #SleepMusic #PianoMusic #Meditation #StressRelief #Relaxation #PeacefulSleep #Mindfulness #CalmingVibes"},
    
    {"title": "Healing Soundscapes 🌿", 
     "description": "Immerse yourself in the healing sounds of nature combined with calming music. This audio blend is ideal for deep relaxation, stress relief, and peaceful meditation. #HealingMusic #Meditation #StressRelief #NatureSounds #Relaxation #Mindfulness #PeacefulSleep #CalmingVibes"},
    
    {"title": "Ocean Breeze Meditation 🌊", 
     "description": "Feel the refreshing breeze of the ocean as it enhances your meditation practice. Let the rhythmic sounds of the waves help you connect with the present moment for deep relaxation. #MeditationMusic #Relaxation #StressRelief #Mindfulness #PeacefulSleep #NatureSounds #OceanBreeze #CalmingVibes"},
    
    {"title": "Binaural Beats for Deep Meditation 🎧", 
     "description": "These binaural beats create a powerful frequency environment to guide you into deep meditation. Ideal for focus, stress relief, and mental clarity. #BinauralBeats #MeditationMusic #StressRelief #Focus #CalmingVibes #MentalClarity #Mindfulness #PeacefulSleep"},
    
    {"title": "Forest Calm and Tranquility 🌳", 
     "description": "Escape into the peaceful ambiance of the forest with calming bird songs and rustling leaves. Perfect for deep relaxation, meditation, or as a serene background during sleep. #ForestSounds #Relaxation #StressRelief #Meditation #Mindfulness #PeacefulMusic #NatureSounds #CalmingVibes"},
    
    {"title": "Healing Rain Sounds for Relaxation 🌧️", 
     "description": "Feel the healing power of gentle rain sounds, perfect for creating a peaceful atmosphere to relax, meditate, and fall into a deep, restorative sleep. #RainSounds #Relaxation #Meditation #StressRelief #SleepMusic #Mindfulness #HealingSounds #PeacefulSleep"},
    
    {"title": "Chimes and Nature for Meditation 🎐", 
     "description": "The soft, melodic sound of wind chimes combined with nature's calming sounds creates the perfect environment for meditation and relaxation. #WindChimes #NatureSounds #MeditationMusic #Relaxation #StressRelief #Mindfulness #CalmingVibes #PeacefulSleep"},
    
    {"title": "Tranquil Night Sounds 🌙", 
     "description": "Let the stillness of the night soothe your mind. Ideal for calming your thoughts, enhancing meditation, or drifting into a peaceful sleep. #NightSounds #Meditation #SleepMusic #Relaxation #StressRelief #Mindfulness #Tranquil #PeacefulSleep"},
    
    {"title": "Zen Meditation Vibes 🧘‍♀️", 
     "description": "A calming mix of Zen-inspired music and nature sounds to guide you into deep meditation, stress relief, and restful sleep. #MeditationMusic #ZenMusic #StressRelief #Relaxation #Mindfulness #PeacefulSleep #CalmingVibes #ZenVibes"},
    
    {"title": "Waterfall Tranquility 🌊", 
     "description": "Let the calming sounds of a waterfall cascade over you, bringing tranquility and relaxation. Ideal for meditation, stress relief, and peaceful sleep. #WaterfallSounds #Meditation #Relaxation #StressRelief #PeacefulMusic #Mindfulness #Tranquility #CalmingVibes"},
    
    {"title": "Crystal Bowls for Healing 🥣", 
     "description": "The healing vibrations of crystal bowls combined with soft melodies guide you into a deeply relaxing state. Perfect for stress relief, meditation, and restful sleep. #SoundHealing #MeditationMusic #StressRelief #Relaxation #CalmingVibes #PeacefulSleep #CrystalBowls #HealingVibes"},
    
    {"title": "Gentle Creek Sounds 🌊", 
     "description": "The soft murmur of a flowing creek provides a peaceful backdrop for meditation or a restful night's sleep, soothing the mind and body. #CreekSounds #MeditationMusic #Relaxation #StressRelief #SleepMusic #NatureSounds #GentleSounds #PeacefulSleep"},
    
    {"title": "Calming Breeze for Deep Sleep 🌬️", 
     "description": "A calming breeze accompanied by gentle sounds creates a peaceful atmosphere that helps promote deep sleep, relaxation, and meditation. #SleepMusic #Meditation #Relaxation #StressRelief #PeacefulSleep #Mindfulness #CalmingBreeze #DeepSleep"},
    
    {"title": "Ocean Symphony for Restful Sleep 🌊", 
     "description": "Immerse yourself in a beautiful ocean symphony designed to promote restful sleep, relaxation, and stress relief with its soothing waves and melodies. #OceanSounds #SleepMusic #Relaxation #Meditation #StressRelief #PeacefulSleep #OceanSymphony #CalmingVibes"},
    
    {"title": "Serenity Through Sound 🌙", 
     "description": "Let serene melodies guide you to inner peace, perfect for meditation, relaxation, and creating a tranquil space for a peaceful night's sleep. #RelaxationMusic #SleepMusic #Meditation #StressRelief #Mindfulness #PeacefulMusic #Serenity #InnerPeace"},
    
    {"title": "Healing Waters for Stress Relief 🌊", 
     "description": "Flowing water sounds paired with soft healing music help soothe your mind and body, ideal for stress relief, meditation, and relaxation. #Meditation #HealingMusic #Relaxation #StressRelief #Mindfulness #PeacefulSleep #HealingWaters #WaterSounds"},
    
    {"title": "Calming Nature Ambience 🌿", 
     "description": "Surround yourself with the natural sounds of birds, rustling leaves, and flowing water to create the perfect atmosphere for deep relaxation and sleep. #NatureSounds #Relaxation #Meditation #StressRelief #SleepMusic #Mindfulness #NatureAmbience #CalmingVibes"},
    
    {"title": "Mystical Forest Sounds 🌳", 
     "description": "Transport yourself to a mystical forest with sounds of whispering trees and gentle breezes, perfect for meditation and creating a peaceful sleep environment. #ForestMusic #Meditation #Relaxation #Mindfulness #StressRelief #PeacefulSleep #MysticalForest #ForestSounds"},
    
    {"title": "Soft Guitar for Deep Relaxation 🎸", 
     "description": "The soft strumming of acoustic guitar combined with peaceful nature sounds helps ease your mind and relax your body, promoting restful sleep. #GuitarMusic #MeditationMusic #StressRelief #Relaxation #PeacefulSleep #AcousticGuitar #DeepRelaxation #CalmingVibes"},
    
    {"title": "Binaural Beats for Focus and Relaxation 🎧", 
     "description": "Let binaural beats guide you to a state of calm focus, perfect for enhancing meditation or improving concentration while relaxing. #BinauralBeats #Meditation #StressRelief #FocusMusic #CalmingVibes #MentalClarity #Focus #Relaxation"},
    
    {"title": "Whale Song for Peaceful Sleep 🐋", 
     "description": "The deep, soothing song of whales creates a calming atmosphere, ideal for relaxation, stress relief, and restful sleep. #OceanSounds #SleepMusic #Relaxation #Meditation #Mindfulness #StressRelief #WhaleSong #PeacefulSleep"},
    
    {"title": "Sunrise Meditation Sounds 🌅", 
     "description": "Wake up with the soothing sounds of a sunrise meditation, perfect for setting a peaceful tone for your day and preparing your mind for mindfulness. #MeditationMusic #Relaxation #StressRelief #MorningVibes #PeacefulSleep #Sunrise #Mindfulness #CalmingVibes"},
    
    {"title": "Healing Soundscapes of the Jungle 🌴", 
     "description": "Let the sounds of the jungle calm your mind, offering a unique soundscape for meditation, stress relief, and peaceful sleep. #JungleSounds #MeditationMusic #StressRelief #Relaxation #PeacefulSleep #JungleAmbience #HealingSounds #NatureSounds"},
    
    {"title": "Moonlight Meditation Vibes 🌙", 
     "description": "Calm your mind under the serene light of the moon with soothing meditation music that promotes relaxation and restful sleep. #MeditationMusic #StressRelief #Mindfulness #CalmingVibes #PeacefulSleep #Moonlight #ZenVibes #Relaxation"},
    
    {"title": "Ambient Rain for Stress Relief 🌧️", 
     "description": "Let the sound of steady rain create a peaceful environment, perfect for meditation, stress relief, and creating the ideal sleep atmosphere. #RainSounds #Relaxation #StressRelief #Meditation #SleepMusic #Mindfulness #AmbientRain #CalmingVibes"},
    
    {"title": "Relaxing Sound of Snowfall ❄️", 
     "description": "Experience the peaceful sound of falling snow, perfect for creating a calming atmosphere for sleep and meditation. #WinterSounds #SleepMusic #Meditation #Relaxation #PeacefulSleep #Mindfulness #Snowfall #CalmingVibes"},
    
    {"title": "Healing Chakra Music 🎶", 
     "description": "This chakra healing music helps balance your energy centers and promotes relaxation, making it perfect for meditation and restful sleep. #ChakraHealing #MeditationMusic #StressRelief #Mindfulness #Relaxation #PeacefulSleep #EnergyHealing #ChakraBalance"},
    
    {"title": "Crystal Clear Waters for Relaxation 💧", 
     "description": "The calming sound of crystal-clear waters flowing creates a peaceful atmosphere ideal for relaxation, meditation, and peaceful sleep. #WaterSounds #MeditationMusic #StressRelief #PeacefulSleep #Relaxation #CrystalWaters #CalmingVibes #Mindfulness"},
    
    {"title": "Solfeggio Frequencies for Meditation 🎶", 
     "description": "Relax to the healing power of Solfeggio frequencies, promoting deep meditation, stress relief, and mental clarity. #SolfeggioFrequencies #StressRelief #MeditationMusic #CalmingVibes #PeacefulMind #HealingFrequencies #Meditation #MentalClarity"},
    
    {"title": "Peaceful Desert Breeze 🌵", 
     "description": "Feel the calming desert breeze and distant sounds of nature, perfect for relaxation, sleep, and meditation. #DesertSounds #Relaxation #MeditationMusic #StressRelief #PeacefulSleep #DesertBreeze #CalmingVibes #Mindfulness"},
    
    {"title": "Soothing Cello for Deep Sleep 🎶", 
     "description": "Soft cello music brings a sense of peace and tranquility, ideal for unwinding, deep sleep, and stress relief. #CelloMusic #Relaxation #SleepMusic #Meditation #StressRelief #DeepSleep #CelloVibes #PeacefulSleep"},
    
    {"title": "Peaceful Rainforest Sounds 🌴", 
     "description": "Transport yourself to the calming depths of the rainforest with sounds of gentle rain, birds, and wildlife, ideal for meditation and peaceful sleep. #RainforestSounds #MeditationMusic #SleepMusic #StressRelief #Relaxation #RainforestAmbience #NatureSounds #PeacefulSleep"},
    
    {"title": "Morning Dew for Mindfulness 🌅", 
     "description": "Awaken to the serene sounds of morning dew and soft birdsongs, perfect for mindfulness meditation and setting a peaceful tone for your day. #NatureSounds #MorningVibes #MeditationMusic #PeacefulSleep #Mindfulness #MorningDew #DawnSounds #CalmingVibes"},
    
    {"title": "Relaxing Harp for Sleep 🎵", 
     "description": "The gentle plucking of harp strings creates a soothing soundscape, ideal for promoting relaxation, sleep, and stress relief. #HarpMusic #MeditationMusic #Relaxation #SleepMusic #StressRelief #HarpVibes #PeacefulSleep #CalmingVibes"},
    
    {"title": "Gentle Breeze and Chimes for Meditation 🎐", 
     "description": "Let the sound of wind chimes and a soft breeze guide you into deep meditation, helping you unwind and create a peaceful environment for sleep. #WindChimes #MeditationMusic #Relaxation #StressRelief #PeacefulSleep #GentleBreeze #ChimeSounds #Mindfulness"}
]

# Comprehensive list of hashtags for the meditation/relaxation niche
all_hashtags = [
    "Meditation", "Mindfulness", "Relaxation", "StressRelief", "PeacefulSleep", 
    "CalmingVibes", "Zen", "SleepMusic", "MeditationMusic", "NatureSounds",
    "OceanSounds", "ForestSounds", "RainSounds", "WindChimes", "BinauralBeats",
    "HealingMusic", "SoundHealing", "PeacefulMusic", "CalmingMusic", "AmbientMusic",
    "ZenMusic", "RelaxationMusic", "SleepSounds", "MeditationVibes", "MindfulLiving",
    "InnerPeace", "MentalClarity", "Focus", "DeepSleep", "RestfulSleep", "Tranquility"
]

def get_random_title_and_description():
    """Returns a random title and description as a tuple."""
    random_text = random.choice(video_texts)
    return random_text["title"], random_text["description"]

def get_random_hashtags(count=30):
    """
    Returns a list of random hashtags for YouTube API tags.
    
    Args:
        count (int): Number of hashtags to return (default: 30)
    
    Returns:
        list: List of random hashtags without the # symbol
    """
    # Shuffle the hashtags and return the requested count
    shuffled_hashtags = all_hashtags.copy()
    random.shuffle(shuffled_hashtags)
    
    # Return the requested number of hashtags (or all if count > available)
    return shuffled_hashtags[:min(count, len(shuffled_hashtags))]

def get_hashtags_from_description(description, count=30):
    """
    Extracts hashtags from a description and returns them as a list.
    
    Args:
        description (str): Description text containing hashtags
        count (int): Maximum number of hashtags to return (default: 30)
    
    Returns:
        list: List of hashtags without the # symbol
    """
    import re
    
    # Find all hashtags in the description
    hashtags = re.findall(r'#(\w+)', description)
    
    # If we don't have enough hashtags, supplement with random ones
    if len(hashtags) < count:
        remaining_count = count - len(hashtags)
        additional_hashtags = get_random_hashtags(remaining_count)
        hashtags.extend(additional_hashtags)
    
    # Return unique hashtags up to the requested count
    unique_hashtags = list(dict.fromkeys(hashtags))  # Preserves order while removing duplicates
    return unique_hashtags[:count]

def get_title_description_and_tags():
    """
    Returns a random title, description, and a list of 30 hashtags.
    
    Returns:
        tuple: (title, description, hashtags_list)
    """
    title, description = get_random_title_and_description()
    hashtags = get_hashtags_from_description(description, 30)
    return title, description, hashtags
