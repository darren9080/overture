from gcp_video_analysis import VideoAnalysis

url_list = ["https://www.youtube.com/watch?v=mN999BUKIzQ",
            "https://www.youtube.com/watch?v=fuFxnHnXl7I",
            "https://www.youtube.com/watch?v=ySkO8uB8BXc",
            "https://www.youtube.com/watch?v=kf22VEkbOo4",
            "https://www.youtube.com/watch?v=Vb_9aatr2fw",
            "https://www.youtube.com/watch?v=g5xzcx5OFaE",
            "https://www.youtube.com/watch?v=ZMOn1SVSnGw",
            "https://www.youtube.com/watch?v=EoH_aBwPMEk",
            "https://www.youtube.com/watch?v=INRAcI0jvjQ",
            "https://www.youtube.com/watch?v=Z3EFFLxkVpA",
            "https://www.youtube.com/watch?v=kyCi-nb409w",
            "https://www.youtube.com/watch?v=MuNiChnHx-U",
            "https://www.youtube.com/watch?v=8DgQYH7cxYQ",
            "https://www.youtube.com/watch?v=bJjyobvT1Tw",
            "https://www.youtube.com/watch?v=EgVbK3qKxR4",
            "https://www.youtube.com/watch?v=EQkuWvwFJss",
            "https://www.youtube.com/watch?v=1oglB9rfYB0",
            "https://www.youtube.com/watch?v=LBdah-mKu2o",
            "https://www.youtube.com/watch?v=XhLRYYeVhlU",
            "https://www.youtube.com/watch?v=6bfvZf2JNNU",
            "https://www.youtube.com/watch?v=M0QMXtTe0Nk",
            "https://www.youtube.com/watch?v=v2OFJZMFJDw",
            "https://www.youtube.com/watch?v=-Ur6mVfMs2w",
            "https://www.youtube.com/watch?v=U2DJCDNhx3E",
            "https://www.youtube.com/watch?v=nSzvr8tSJd8",
            "https://www.youtube.com/watch?v=U916LEz-_3s",
            "https://www.youtube.com/watch?v=JAAOqkxAFM8",
            "https://www.youtube.com/watch?v=7cP_rTSEll0",
            "https://www.youtube.com/watch?v=aeuuSl2cahU",
            "https://www.youtube.com/watch?v=l0Twwh_YhcE",
            "https://www.youtube.com/watch?v=jTYuM_2Plps",
            "https://www.youtube.com/watch?v=9l9ra59ob80",
            "https://www.youtube.com/watch?v=RjVKHESypQA",
            "https://www.youtube.com/watch?v=Tww28Hpp4tI",
            "https://www.youtube.com/watch?v=7yjCeGTCJFA",
            "https://www.youtube.com/watch?v=0x65nOjrC5I",
            "https://www.youtube.com/watch?v=WTyX22sSGss",
            "https://www.youtube.com/watch?v=3ERL5_c-tI8",
            "https://www.youtube.com/watch?v=ii2Pb8HXU8s",
            "https://www.youtube.com/watch?v=NHBt5qDfGHc",
            "https://www.youtube.com/watch?v=IdtY0waRuUc",
            "https://www.youtube.com/watch?v=P3mdy6iLQaI",
            "https://www.youtube.com/watch?v=rJRzMFeN8z0",
            "https://www.youtube.com/watch?v=ZMXRMYB1mZI",
            "https://www.youtube.com/watch?v=gAVmbGNqgiw",
            "https://www.youtube.com/watch?v=QaFbPdPwZNk",
            "https://www.youtube.com/watch?v=cba6Jiq2uZM",
            "https://www.youtube.com/watch?v=8_agLbvYN9M",
            "https://www.youtube.com/watch?v=L2YcUcPjq30",
            "https://www.youtube.com/watch?v=sbXvVVmDrmc",
            "https://www.youtube.com/watch?v=vC0mt_iS4SY",
            "https://www.youtube.com/watch?v=XD-bwEsyxqk",
            "https://www.youtube.com/watch?v=BO1kgIFafIA",
            "https://www.youtube.com/watch?v=6bf4c-qDmUk",
            "https://www.youtube.com/watch?v=PkqYenzt5K0",
            "https://www.youtube.com/watch?v=SZH0R_Nkvig",
            "https://www.youtube.com/watch?v=xinLPq04IRM",
            "https://www.youtube.com/watch?v=t6sIV_fTi9E",
            "https://www.youtube.com/watch?v=d_PgjEWyzjQ",
            "https://www.youtube.com/watch?v=3n-UBQJrMKo",
            "https://www.youtube.com/watch?v=dex98dHO1I8",
            "https://www.youtube.com/watch?v=tPPkPRInZp4",
            "https://www.youtube.com/watch?v=wTLtn3qLy4Y",
            "https://www.youtube.com/watch?v=ITPS_SGOQj8",
            "https://www.youtube.com/watch?v=I41kXWb2nyA",
            "https://www.youtube.com/watch?v=zOE9Pp56gJA",
            "https://www.youtube.com/watch?v=OsG3J9myBqg",
            "https://www.youtube.com/watch?v=1oglB9rfYB0",
            "https://www.youtube.com/watch?v=RwT4qB7dSQA",
            "https://www.youtube.com/watch?v=LK6dQc_fOqg",
            "https://www.youtube.com/watch?v=bpA6927C_Oo",
            "https://www.youtube.com/watch?v=GS5VwaTm42k",
            "https://www.youtube.com/watch?v=g-_sKNFl_to",
            "https://www.youtube.com/watch?v=0ohaUQxYVxg",
            "https://www.youtube.com/watch?v=r78pheO3yKs",
            "https://www.youtube.com/watch?v=4i7ro_z763s",
            "https://www.youtube.com/watch?v=8jgGy_ZBHVs",
            "https://www.youtube.com/watch?v=kglHcl7n_8E",
            "https://www.youtube.com/watch?v=Vq1Ind-rQqI",
            "https://www.youtube.com/watch?v=2KG0B_PEqPg",
            "https://www.youtube.com/watch?v=mqzYuZoRM2E",
            "https://www.youtube.com/watch?v=nLTZQHIwH5M",
            "https://www.youtube.com/watch?v=2mEHd_dgXr8",
            "https://www.youtube.com/watch?v=iALTidMT5B8",
            "https://www.youtube.com/watch?v=nHfDWNlnaN4",
            "https://www.youtube.com/watch?v=utG72nChJfs",
            "https://www.youtube.com/watch?v=rRoM04WNmdk",
            "https://www.youtube.com/watch?v=yxtqPJqXxMo",
            "https://www.youtube.com/watch?v=58t9p2bpK6Y",
            "https://www.youtube.com/watch?v=bjpS3JgxcMQ",
            "https://www.youtube.com/watch?v=674JKGg0wMk",
            "https://www.youtube.com/watch?v=Cj2cZx1eQC4",
            "https://www.youtube.com/watch?v=Na1vq2Buamc",
            "https://www.youtube.com/watch?v=x0GzJybg7fA",
            "https://www.youtube.com/watch?v=_MJbfkXZVkQ",
            "https://www.youtube.com/watch?v=Cj7pSc0AE9U",
            "https://www.youtube.com/watch?v=AT09D97JpFA",
            "https://www.youtube.com/watch?v=LGq97Krg5jc",
            "https://www.youtube.com/watch?v=UggBVHCmKSo",
            "https://www.youtube.com/watch?v=5bNNmnL_-Zo"]



title_list = ["GoPro Hero 7 Hypersmooth at 4K Motorcycle Ride",
              "GoPro HERO8 Black: Cre8ors Hypersmooth 2.0 Madness",
              "Testing out the GoPro Hero 7 Black Edition.",
              "4K GoPro Hero 7 Black 4:3 HyperSmooth! || Review! || Vlog Ep. 1",
              "GoPro HERO7 Black: Hypersmooth Gamechanger & Giveaway!",
              "Hypersmooth is awsome / GoPro Hero7black VLOG 20",
              "Disney World November 2018 vlog GoPro hero 7 Black Hypersmooth",
              "GoPro Hero 7 Black Review for MTB Footage - Hyper Smooth, Superb Audio & Video and best settings",
              "4K All New GoPro Hypersmooth Stabilization Feature Vlog at Sea World Orlando",
              "Vlog #Life Test Nouvelle GoPro Black 7 TimeWarp Hypersmooth",
              "HYPERSMOOTH trail walking vlog with GoPro",
              "A Day by GoPro Hero7black I Hypersmooth #VLOG 15",
              "Running Tour at Huntington Beach | Hypersmooth GoPro | Running Vlog | The Delsol Runner",
              "GoPro Hero 7 Black | Vlog Test (Hypersmooth + Timewarp) | Welcome to our CHANNEL!",
              "My Holiday in Fuerteventura | Travel Vlog #1 - GoPro Hero 7 Black",
              "Gopro hero 7 black - Hypersmooth - TimeWrap - Mount Cook 2018",
              "HERO7 HyperSmooth - Kauai Helicopter Adventure",
              "HERO7 TimeWarp - Hyperlapse without a Gimbal",
              "GoPro Hero 7 Timewarp / Hyperlapse",
              "HyperSmooth Cam Fitzpatrick Top to Bottom Run at Jackson Hole with GoPro HERO7",
              "Gopro Hero 7 Dirt Bike hypersmooth",
              "GoPro #Hero7 on a Dirt Bike Hypersmooth 4k 60fps + Audio Test",
              "GoPro Hero 7 Black HyperSmooth in 4K Street Bike Test",
              "GoPro Hero 8 Black 4k Hypersmooth 2.0 Raw Footage",
              "[4K] Disney's Roller Coasters GoPro Hero 7 Hypersmooth Test - Disneyland",
              "Riding Yamaha R1 With GoPro Hero 7 Hypersmooth",
              "GoPro Hero7 HyperSmooth Test - 60 MPH+ RC Car",
              "GoPro Hero 7 Hypersmooth Mtb Test (4k 60Fps)",
              "HyperSmooth on S1000RR - BLOWN AWAY! - GoPro Hero 7 Black",
              "GoPro Hero7 Black: Mountain Biking with HyperSmooth in Schladming",
              "Testing Out My New GoPro. (HERO7 + HyperSmooth)",
              "🚗 GoPro HERO 7 BLACK Hypersmooth : FUNCIONA?",
              "FPV Cloud Surfing Long Range Drone | GoPro Hero 7 Hypersmooth |",
              "Shorebreak 4K GoPro 7 Black 60fps HyperSmooth",
              "Exploring Lisbon (GoPRO HERO7 HyperSmooth Test)",
              "Video test GoPro Hero 7 Black - 4K 60fps - HyperSmooth Stbilization",
              "GoPro Hero 7 Black - HyperSmooth Skiing at Park City Utah",
              "GoPro Hero 7 Black Test - MTB Downhill with Hypersmooth 1080 30fps",
              "Airsoft with GoPro HERO7 HyperSmooth Enabled",
              "GoPro Hero 7 - Hypersmooth Skiing in 4K",
              "GoPro 7 black HyperSmooth 60fps - kayaking in Norway",
              "GoPro Hero 7: Hypersmooth skiing in Flachau | Dji Mavic 2 Pro | in 4K",
              "HYPERSMOOTH GoPro Hero 7 Black + RC Plane",
              "4K | GoPro Hero 7 Black Hypersmooth Test Demo",
              "Hero 7 Gopro Hypersmooth with FeiyuTech WG2 3 Axis Gimbal on Stanley Gap 4K",
              "Gopro hero 7 black test - how works the hypersmooth stabilization for speedflying?",
              "GoPro Hero7 Black - HyperSmooth Demo",
              "GoPro HERO 7 Black | HyperSmooth 4K",
              "GoPro Hero 7 Test - Hypersmooth on my worst quad",
              "GoPro Hero 7 - Hypersmooth test skiing in 4k",
              "Drone Flying in Forest | FPV Flying - Hypersmooth GoPro 7 4K",
              "GoPro: Corfu - Greece (GoPro Hero 7 & Hypersmooth)",
              "VIBRATIONS // GOPRO HERO 7 // HYPERSMOOTH",
              "GoPro Hypersmooth + FPV Wing on a Windy Day",
              "GoPro Hero7 Black HyperSmooth Yamaha Raptor 700 ATV Riding Rattlesnake Ridge Motovlog TrailBlogger",
              "GoPro Hero 7 Black on Dog with Hypersmooth Test",
              "GoPro Hero 7 HyperSmooth on Whistler's A-Line",
              "Balade d'Automne avec la GoPro Hero 7 Black + Hypersmooth #Ride 63 [EN SUBS]",
              "[4k 60FPS] Cheetah Hunt Front Row wih HYPERSMOOTH GoPro Hero 7 Black!",
              "GoPro Hero 7 Black, 4k/60fps/HyperSmooth/Yamaha Grizzly 660 Snow Ride!",
              "GoPro Hero 7 Black Hypersmooth sample 4k 60Fps walking to Diagon Alley Universal Studios Florida",
              "(Airsoft Game) 2018.09.30, Bergen - Gopro Hero 7 Black, HyperSmooth Stabilisation Video Footage!",
              "test Gopro Hero 7 - Hypersmooth Kitesurf - Beauduc Sunset",
              "Malediven 2019 🌴 I am in Paradise 🌴 GoPro Hero 7 Black Hypersmooth - Island Kuramathi",
              "Hero 7 Hypersmooth With Gimbal Motorcycle Ride",
              "Nakiska | Snowboarding (GoPro Hero 7 Black Test) Cinematic Hypersmooth",
              "First Rip GoPro Hero 7 Black HyperSmooth 2 7k 60FPS Linear",
              "HERO7 HyperSmooth - Kauai Helicopter Adventure",
              "GoPro Hero7 Kayak Hypersmooth",
              "[4k 60fps] Mako Front Row HYPERSMOOTH GoPro Hero 7 Black!",
              "GoPro HERO7 BLACK - TIME WARP TESTS & HYPERSMOOTH MAGIC",
              "Test de la Kawasaki Vulcan S en 4k 60fps HyperSmooth 🙄 GoPro Hero 7 Black !",
              "GoPro Hero 7 Black - 4K Hypersmooth running and jumping!",
              "GoPro hero 7 black Mountain biking in 4K Hypersmooth",
              "Gopro Hero 7 Black HYPERSMOOTH !",
              "GoPro Hero 7 Black - Hypersmooth FPV Test Flight.",
              "GoPro Hero 7 HyperSmooth stabilization on a dirtbike",
              "GoPro HERO 7 BLACK PARKOUR TEST HYPERSMOOTH + KARMA GRIP QUEBEC 4K",
              "GoPro Hero 7 Hypersmooth test: Rough Trail & Hardtail - Mountain Bike Austin",
              "Gopro Hero 7 HyperSmooth - RAW",
              "GoPro HyperSmooth Kids Snow Day",
              "GOPRO HERO 7 HYPERSMOOTH PARKOUR | Parkour POV",
              "GoPro 7 HyperSmooth slow motion Kayaking in Norway",
              "Travel Rhodes 2018 | Gopro Hero 7 Black | HyperSmooth",
              "Gopro 7 Paragliding Test 4k 60p Hypersmooth",
              "GoPro 7 hypersmooth FAIL in low light - MTB",
              "GoPro Hero 7 Black 2.7K 60fps Superview Hypersmooth paragliding test",
              "Trail run Gopro 7 Black headmount hypersmooth test",
              "Downhill Testride Gopro 7 - Hypersmooth",
              "USA 2019 | GoPro Hero 7 Black - 4k 60fps & Hypersmooth",
              'GMP Adelboden Lenk "Spring Hype" - GoPro Hypersmooth 4K',
              "GOPRO HERO 7 BLACK - ENDURO MOTOCROSS - HYPERSMOOTH STABILIZATION TEST",
              "Gopro Hero 7 Hypersmooth Skiing",
              "Ar wing with gopro 7 hypersmooth",
              "Gopro Hero 7 black 4k 24fps Hypersmooth",
              "Gopro Hero 7: KARMA + HERO7 (HYPERSMOOTH DRONE FOOTAGE)",
              "GoPro HERO7 Black 1080p 60fps HYPERSMOOTH Footage Paris",
              "Silver Star 4K Onride Gopro Hero 7 #Hypersmooth / Low Light Test - Europa-Park",
              "GoPro Hero7 HyperSmooth手ぶれ補正 手持ち＆ジンバル比較",
              "Rough Arizona Sand Track with GoPro Hypersmooth"]


VA = VideoAnalysis()

for url, title in zip(url_list, title_list):
    file_dir, file_name = VA.download_video(url, title)
    VA.analyze_video(file_dir, file_name)
