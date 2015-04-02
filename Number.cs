using System;

namespace wodehouse
{
    public class Number : Expression
    {
        public string StringValue;

        public long AsLong()
        {
            throw new NotImplementedException();
        }

        public double AsDouble()
        {
            throw new NotImplementedException();
        }

        public decimal AsDecimal()
        {
            throw new NotImplementedException();
        }
    }
}
