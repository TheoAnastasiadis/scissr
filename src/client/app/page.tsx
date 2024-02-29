import Image from "next/image";
import HomePageNavBar from "@/components/navigation/HomePageNavbar";
import ContentSection from "@/components/branding/content/contentSection";
import { Spotlight } from "@/components/aceternity/spotlight";
import { Button, Card, CardFooter, CardHeader } from "@nextui-org/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUserPlus, faArrowRight } from "@fortawesome/free-solid-svg-icons";
import {
  CardContainer,
  CardItem,
  CardBody,
} from "@/components/aceternity/3dcard";
import HomePageHero from "@/components/pages/homePage/hero";
import Featured from "@/components/pages/homePage/featured";
import Promo from "@/components/pages/homePage/promo";
import HomePageFooter from "@/components/navigation/HomePageFooter";

export default function Home() {
  const features = [
    {
      title: "Easily find matches in your area",
      body: "Very exciting feature",
      img: "https://plus.unsplash.com/premium_photo-1667490646793-3e2bfe0927ac?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      action: "Explore grid view now",
    },
    {
      title: "Filter people by your criteria and interests",
      body: "Very exciting feature",
      img: "https://images.unsplash.com/photo-1485586752437-03021cfb7ea4?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      action: "Explore vibes now",
    },
    {
      title: "Make lasting connections",
      body: "Very exciting feature",
      img: "https://plus.unsplash.com/premium_photo-1679865370726-0582e8630f64?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
      action: "Get started",
    },
  ];

  return (
    <>
      <HomePageNavBar />
      <HomePageHero />
      <section className="container">
        <ContentSection
          title="Lorem ipsum dolor, sit amet consectetur adipisicing elit. "
          subtitle="Lorem ipsum dolor, sit amet consectetur adipisicing elit."
          body={[
            "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Libero iure quasi quae architecto culpa nesciunt cum, cumque illo qui reiciendis, numquam, at ipsa iusto inventore ea sed nemo asperiores magnam.",
            "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Libero iure quasi quae architecto culpa nesciunt cum, cumque illo qui reiciendis, numquam, at ipsa iusto inventore ea sed nemo asperiores magnam.",
          ]}
        ></ContentSection>
      </section>
      <Featured />
      <Promo />
      <HomePageFooter />
    </>
  );
}
