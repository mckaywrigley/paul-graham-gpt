import { IconExternalLink } from "@tabler/icons-react";
import { FC } from "react";

export const Navbar: FC = () => {
  return (
    <div className="flex h-[60px] border-b border-gray-300 py-2 px-8 items-center justify-between">
      <div className="font-bold text-2xl flex items-center">
        <a
          className="text-slate-50 hover:opacity-80"
          // TODO: // Change this to the current webpage
          href="http://localhost:3000/"
        >
          Setori
        </a>
      </div>
      <div>
        <a
          className="flex items-center text-slate-50 hover:opacity-80"
          href="https://www.setori.ai/"
          target="_blank"
          rel="noreferrer"
        >
          <div className="hidden sm:flex">setori.ai</div>

          <IconExternalLink
            className="ml-1"
            size={20}
          />
        </a>
      </div>
    </div>
  );
};
