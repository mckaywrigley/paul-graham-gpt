import { IconBrandLinkedin, IconBrandTwitter } from "@tabler/icons-react";
import { FC } from "react";

export const Footer: FC = () => {
  return (
    <div className="flex h-[50px] border-t border-gray-300 py-2 px-8 items-center sm:justify-between justify-center">
      <div className="hidden sm:flex"></div>

      <div className="hidden sm:flex italic text-sm text-slate-50">
        Crafted by
        <a
          className="hover:opacity-80 mx-1"
          href="https://twitter.com/mckaywrigley"
          target="_blank"
          rel="noreferrer"
        >
          Setori
        </a>
        & inspired by
        <a
          className="hover:opacity-80 ml-1"
          href="https://twitter.com/mckaywrigley"
          target="_blank"
          rel="noreferrer"
        >
          Mckay Wrigley
        </a>
        .
      </div>

      <div className="flex space-x-4">
      <a
          className="flex items-center text-slate-50 hover:opacity-80"
          href="https://www.linkedin.com/company/91703932"
          target="_blank"
          rel="noreferrer"
        >
          <IconBrandLinkedin size={24} />
        </a>
        <a
          className="flex items-center text-slate-50 hover:opacity-80"
          href="https://twitter.com/setoriai"
          target="_blank"
          rel="noreferrer"
        >
          <IconBrandTwitter size={24} />
        </a>
      </div>
    </div>
  );
};
