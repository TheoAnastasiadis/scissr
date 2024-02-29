export default function ContentSection(props: {
  title?: string;
  subtitle?: string;
  body: string[] | JSX.Element;
}) {
  return (
    <section className="my-5">
      <div className=" flex flex-col items-center px-5 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div className="flex flex-col w-full max-w-3xl mx-auto prose text-left prose-blue">
          <div className="w-full mx-auto space-y-10">
            {props.title ? (
              <h1 className="text-5xl">{props.title}</h1>
            ) : undefined}
            {props.subtitle ? (
              <h2 className="text-3xl">{props.subtitle}</h2>
            ) : undefined}
            {Array.isArray(props.body) ? (
              <div className="space-y-5">
                {props.body.map((p, i) => (
                  <p key={i}>{p}</p>
                ))}
              </div>
            ) : (
              props.body
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
