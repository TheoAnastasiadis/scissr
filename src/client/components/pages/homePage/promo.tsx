import ContentSection from "@/components/branding/content/contentSection";
import { faGlobe } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Button, Card, CardHeader } from "@nextui-org/react";

export default function Promo() {
  return (
    <section className="container my-14 flex flex-row justify-around max-w-5xl mx-auto">
      <div className="w-1/2 flex flex-col justify-center">
        <ContentSection
          subtitle="Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolores nemo quaerat pariatur veniam dolorum!"
          body={
            <div className="w-full space-y-5">
              <Button endContent={<FontAwesomeIcon icon={faGlobe} />}>
                Open WebView
              </Button>
            </div>
          }
        ></ContentSection>
      </div>
      <div className="w-1/2 p-10">
        <Card className="h-96">
          <CardHeader className="pb-0 pt-2 px-4 flex-col items-start">
            <p className="text-tiny uppercase font-bold">Daily Mix</p>
            <small className="text-default-500">12 Tracks</small>
            <h4 className="font-bold text-large">Frontend Radio</h4>
          </CardHeader>
        </Card>
      </div>
    </section>
  );
}
