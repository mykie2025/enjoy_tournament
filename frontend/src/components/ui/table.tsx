import * as React from 'react';

interface TableProps extends React.HTMLAttributes<HTMLTableElement> {}
export function Table({ className = '', children, ...props }: TableProps) {
  return (
    <table className={`min-w-full divide-y divide-gray-200 ${className}`} {...props}>
      {children}
    </table>
  );
}

interface TableHeaderProps extends React.HTMLAttributes<HTMLTableSectionElement> {}
export function TableHeader({ className = '', children, ...props }: TableHeaderProps) {
  return (
    <thead className={`bg-gray-50 ${className}`} {...props}>
      {children}
    </thead>
  );
}

interface TableBodyProps extends React.HTMLAttributes<HTMLTableSectionElement> {}
export function TableBody({ className = '', children, ...props }: TableBodyProps) {
  return (
    <tbody className={`${className}`} {...props}>
      {children}
    </tbody>
  );
}

interface TableRowProps extends React.HTMLAttributes<HTMLTableRowElement> {}
export function TableRow({ className = '', children, ...props }: TableRowProps) {
  // Filter out any whitespace string nodes to prevent illegal text nodes in <tr>
  const filteredChildren = React.Children.toArray(children).filter(
    (child) => typeof child !== 'string'
  );
  return (
    <tr className={className} {...props}>
      {filteredChildren}
    </tr>
  );
}

interface TableHeadProps extends React.ThHTMLAttributes<HTMLTableCellElement> {}
export function TableHead({ className = '', children, ...props }: TableHeadProps) {
  return (
    <th
      scope="col"
      className={`px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider ${className}`} 
      {...props}
    >
      {children}
    </th>
  );
}

interface TableCellProps extends React.TdHTMLAttributes<HTMLTableCellElement> {}
export function TableCell({ className = '', children, ...props }: TableCellProps) {
  return (
    <td className={`px-6 py-4 whitespace-nowrap ${className}`} {...props}>
      {children}
    </td>
  );
}
