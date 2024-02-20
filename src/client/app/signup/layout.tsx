export default function SignUpLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="h-screen aspect-[9/16] bg-black-500 my-5 mx-auto rounded-3xl p-10">
      {children}
    </div>
  );
}
