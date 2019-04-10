import java.awt.List;

//This class provides a few static create operators, equality tests, and 
//computes the hash from a byte array, string, or two other MerkleHash instances.
public class MerkleHash {
	//subject to change
	private int[] Value;

    protected MerkleHash()
    {
    }

    public static MerkleHash Create(byte[] buffer)
    {
      MerkleHash hash = new MerkleHash();
      hash.ComputeHash(buffer);

      return hash;
    }

    public static MerkleHash Create(String buffer)
    {
      return Create(Encoding.UTF8.GetBytes(buffer));
    }

    public static MerkleHash Create(MerkleHash left, MerkleHash right)
    {
      return Create(left.Value.Concat(right.Value).ToArray());
    }

    public static boolean equals(MerkleHash h1, MerkleHash h2)
    {
      return h1.equals(h2);
    }

    public static boolean notEqual(MerkleHash h1, MerkleHash h2)
    {
      return !h1.equals(h2);
    }

    public int GetHashCode()
    {
      return super.hashCode();
    }

    public boolean equals(Object obj)
    {
  //implement the contract method
    	MerkleTree.Contract(() => obj is MerkleHash, "rvalue is not a MerkleHash");
      return Equals((MerkleHash)obj);
    }

//how to get rid of the error?? add package
    public void ComputeHash(byte[] buffer)
    {
      SHA256 sha256 = SHA256.Create();
      SetHash(sha256.ComputeHash(buffer));
    }

    public void SetHash(byte[] hash)
    {
      MerkleTree.Contract(() => hash.Length == Constants.HASH_LENGTH, "Unexpected hash length.");
      Value = hash;
    }
//other equals methods
 /*   public bool Equals(byte[] hash)
    {
      return Value.SequenceEqual(hash);
    }

    public bool Equals(MerkleHash hash)
    {
      bool ret = false;

      if (((object)hash) != null)
      {
        ret = Value.SequenceEqual(hash.Value);
      }

      return ret;
    }
  }
}*/
    
 //build tree from its leaves:
    public MerkleHash BuildTree()
    {
      // We do not call FixOddNumberLeaves because we want the ability to append 
      // leaves and add additional trees without creating unecessary wasted space in the tree.
      Contract(() => leaves.Count > 0, "Cannot build a tree with no leaves.");
      BuildTree(leaves);

      return RootNode.Hash;
    }

    /// <summary>
    /// Recursively reduce the current list of n nodes to n/2 parents.
    /// </summary>
    /// <param name="nodes"></param>
    protected void BuildTree(List<MerkleNode> nodes)
    {
      Contract(() => nodes.Count > 0, "node list not expected to be empty.");

      if (nodes.Count == 1)
      {
        RootNode = nodes[0];
      }
      else
      {
        List<MerkleNode> parents = new List<MerkleNode>();

        for (int i = 0; i < nodes.Count; i += 2)
        {
          MerkleNode right = (i + 1 < nodes.Count) ? nodes[i + 1] : null;
          MerkleNode parent = CreateNode(nodes[i], right);
          parents.Add(parent);
        }

        BuildTree(parents);
      }
    }
    
    //appending leaves
/*    public MerkleNode AppendLeaf(MerkleNode node)
    {
      nodes.Add(node);
      leaves.Add(node);

      return node;
    }

    public void AppendLeaves(MerkleNode[] nodes)
    {
      nodes.ForEach(n => AppendLeaf(n));
    }

    public MerkleNode AppendLeaf(MerkleHash hash)
    {
      MerkleNode node = CreateNode(hash);
      nodes.Add(node);
      leaves.Add(node);

      return node;
    }

    public List<MerkleNode> AppendLeaves(MerkleHash[] hashes)
    {
      List<MerkleNode> nodes = new ArrayList<MerkleNode>();
      hashes.ForEach(h => nodes.Add(AppendLeaf(h)));

      return nodes;
    }*/
}
