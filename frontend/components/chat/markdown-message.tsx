import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type MarkdownMessageProps = {
  content: string;
};

export function MarkdownMessage({
  content,
}: MarkdownMessageProps) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        h1: ({ children }) => (
          <h1 className="mb-4 mt-6 text-2xl font-bold tracking-tight">
            {children}
          </h1>
        ),

        h2: ({ children }) => (
          <h2 className="mb-3 mt-5 text-xl font-semibold tracking-tight">
            {children}
          </h2>
        ),

        h3: ({ children }) => (
          <h3 className="mb-2 mt-4 text-base font-semibold">
            {children}
          </h3>
        ),

        p: ({ children }) => (
          <p className="mb-3 leading-7 text-foreground/90">
            {children}
          </p>
        ),

        ul: ({ children }) => (
          <ul className="mb-4 ml-5 list-disc space-y-2">
            {children}
          </ul>
        ),

        ol: ({ children }) => (
          <ol className="mb-4 ml-5 list-decimal space-y-2">
            {children}
          </ol>
        ),

        li: ({ children }) => (
          <li className="leading-7 text-foreground/90">
            {children}
          </li>
        ),

        strong: ({ children }) => (
          <strong className="font-semibold text-foreground">
            {children}
          </strong>
        ),

        blockquote: ({ children }) => (
          <blockquote className="my-4 border-l-4 border-primary/30 pl-4 italic text-muted-foreground">
            {children}
          </blockquote>
        ),

        code: ({ children }) => (
          <code className="rounded bg-muted px-1.5 py-0.5 font-mono text-sm">
            {children}
          </code>
        ),

        pre: ({ children }) => (
          <pre className="my-4 overflow-x-auto rounded-xl bg-zinc-950 p-4 text-sm text-zinc-100">
            {children}
          </pre>
        ),

        hr: () => (
          <hr className="my-6 border-border" />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
}